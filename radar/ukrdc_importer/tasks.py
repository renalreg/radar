import logging

from celery import shared_task
from cornflake.exceptions import ValidationError
import sqlalchemy

from radar.database import db
from radar.models.groups import Group, GROUP_TYPE
from radar.models.logs import Log
from radar.models.patient_locks import PatientLock
from radar.models.patients import Patient
from radar.ukrdc_importer.addresses import import_addresses
from radar.ukrdc_importer.aliases import import_aliases
from radar.ukrdc_importer.demographics import import_demographics
from radar.ukrdc_importer.medications import import_medications
from radar.ukrdc_importer.patient_numbers import import_patient_numbers
from radar.ukrdc_importer.results import import_results
from radar.ukrdc_importer.serializers import ContainerSerializer
from radar.ukrdc_importer.utils import get_import_user


logger = logging.getLogger(__name__)

QUEUE = 'ukrdc_importer'


def find_patient_ids(sda_patient_numbers):
    """Find the patient ids in the list of patient numbers."""

    system_codes = [x.code for x in Group.query.filter(Group.type == GROUP_TYPE.SYSTEM)]
    numbers = []

    for sda_patient_number in sda_patient_numbers:
        if sda_patient_number['organization']['code'] in system_codes:
            numbers.append(sda_patient_number['number'])

    return numbers or None


def parse_patient_id(value):
    """Check the patient id is an integer."""

    if isinstance(value, basestring):
        value = int(value)

    return value


def get_patient(patient_id):
    """Get a patient by id."""

    return Patient.query.get(patient_id)


def lock_patient(patient):
    """Lock a patient."""

    while True:
        # Attempt to lock this patient
        # Blocks until we have a lock or returns None on first import
        patient_lock = PatientLock.query.filter(PatientLock.patient == patient).with_for_update().first()

        # Lock acquired
        if patient_lock is not None:
            return patient_lock
        else:
            # First import, create a row for this patient in the locks table
            try:
                session = db.session.session_factory()
                patient_lock = PatientLock()
                patient_lock.patient = session.merge(patient)
                session.add(patient_lock)
                session.commit()
            except sqlalchemy.exc.IntegrityError:
                pass


def log_data_import(patient, raw=False):
    log = Log()
    log.type = 'UKRDC_IMPORTER'
    log.user = get_import_user()
    if raw:
        log.data = patient
        log.data['container'] = True
    else:
        log.data = {'patient_id': patient.id}
    db.session.add(log)


@shared_task(ignore_result=True, queue=QUEUE)
def import_sda(data, sequence_number, patient_id=None):
    # Note about data types:
    # The code that produces SDA JSON files in the UKRDC determines types based on the
    # content of the value.
    # A value that is all digits will be sent as a JSON number.
    # e.g. If a patient's name is "123" it will be sent as a JSON number not a JSON string.
    # Potentially any value in the SDA JSON can be sent as a JSON number.
    # There seem to be only two data types in SDA: numbers (%Library.Numeric) and strings (%Library.String).
    # Almost all values are strings (%Library.String).

    serializer = ContainerSerializer()

    # Check the file matches enough of the schema to be imported
    try:
        sda_container = serializer.run_validation(data)
    except ValidationError as e:
        logger.error('Container is invalid errors={errors}'.format(errors=e.flatten()))
        return False

    sda_patient = sda_container['patient']
    sda_patient_numbers = sda_patient['patient_numbers']

    # No patient ID supplied
    if patient_id is None:
        patient_ids = find_patient_ids(sda_patient_numbers)

        # No patient ID in file
        if patient_ids is None:
            logger.error('Patient ID is missing. Data - %s', sda_container)
            return False

        if len(set(patient_ids)) > 1:
            string_ids = [str(pat_id) for pat_id in patient_ids]
            logger.error('Multiple patient IDs returned - {}'.format('; '.join(string_ids)))
            return False

        patient_id = patient_ids[0]

        # Check the format of the patient ID
        try:
            patient_id = parse_patient_id(patient_id)
        except ValueError:
            logger.error('Patient ID is invalid id={id}'.format(id=patient_id))
            return False

    # Get the patient by their ID
    patient = get_patient(patient_id)

    # Patient not found (possibly the patient was deleted)
    if patient is None:
        logger.error('Patient not found id={id}'.format(id=patient_id))
        return False

    # Lock the patient while we import the data
    # Simulatenous updates could result in inconsistency otherwise
    patient_lock = lock_patient(patient)

    # Check we haven't already imported a newer sequence number
    if patient_lock.sequence_number is not None and sequence_number < patient_lock.sequence_number:
        logger.info('Skipping old sequence number {0} < {1}'.format(sequence_number, patient_lock.sequence_number))
        return False

    patient_lock.sequence_number = sequence_number

    sda_names = sda_patient.get('aliases', list())
    sda_addresses = sda_patient.get('addresses', list())
    sda_medications = sda_container.get('medications', list())
    sda_lab_orders = sda_container.get('lab_orders', list())

    if patient.id == 8241:
        log_data_import(sda_container, raw=True)

    import_demographics(patient, data['patient'])
    import_patient_numbers(patient, sda_patient_numbers)
    import_aliases(patient, sda_names)
    import_addresses(patient, sda_addresses)
    import_medications(patient, sda_medications)
    import_results(patient, sda_lab_orders)

    log_data_import(patient)

    db.session.commit()

    return True
