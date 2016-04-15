import logging

import sqlalchemy
from celery import Celery
from jsonschema import validate, ValidationError

from radar.models.patients import Patient
from radar.models.patient_locks import PatientLock
from radar.database import db

from radar_ukrdc_importer.aliases import import_aliases
from radar_ukrdc_importer.medications import import_medications
from radar_ukrdc_importer.addresses import import_addresses
from radar_ukrdc_importer.demographics import import_demographics
from radar_ukrdc_importer.patient_numbers import import_patient_numbers
from radar_ukrdc_importer.results import import_results
from radar_ukrdc_importer.utils import load_schema


logger = logging.getLogger(__name__)

celery = Celery()


def find_patient_id(sda_patient_numbers):
    """Find RaDaR number in patient numbers"""

    for sda_patient_number in sda_patient_numbers:
        if sda_patient_number['organization']['code'] == 'RADAR':
            return sda_patient_number['number']

    return None


def parse_patient_id(value):
    if isinstance(value, basestring):
        value = int(value)

    return value


def get_patient(patient_id):
    return Patient.query.get(patient_id)


def lock_patient(patient):
    while True:
        patient_lock = PatientLock.query.filter(PatientLock.patient == patient).with_for_update().first()

        if patient_lock is not None:
            return patient_lock
        else:
            try:
                session = db.session.session_factory()
                patient_lock = PatientLock()
                patient_lock.patient = session.merge(patient)
                session.add(patient_lock)
                session.commit()
            except sqlalchemy.exc.IntegrityError:
                pass


@celery.task
def import_sda(sda_container, sequence_number):
    schema = load_schema('schema.json')

    try:
        validate(sda_container, schema)
    except ValidationError:
        logger.error('Container is invalid')
        return False

    sda_patient = sda_container['patient']
    sda_patient_numbers = sda_patient['patient_numbers']

    patient_id = find_patient_id(sda_patient_numbers)

    if patient_id is None:
        logger.error('Patient ID is missing')
        return False

    try:
        patient_id = parse_patient_id(patient_id)
    except ValueError:
        logger.error('Patient ID is invalid id={id}'.format(id=patient_id))
        return False

    patient = get_patient(patient_id)

    if patient is None:
        logger.error('Patient not found id={id}'.format(id=patient_id))
        return False

    patient_lock = lock_patient(patient)

    if patient_lock.sequence_number is not None and sequence_number < patient_lock.sequence_number:
        logger.info('Skipping old sequence number {0} < {1}'.format(sequence_number, patient_lock.sequence_number))
        return False

    patient_lock.sequence_number = sequence_number

    sda_names = sda_patient.get('aliases', list())
    sda_addresses = sda_patient.get('addresses', list())
    sda_medications = sda_container.get('medications', list())
    sda_lab_orders = sda_container.get('lab_orders', list())

    import_demographics(patient, sda_patient)
    import_patient_numbers(patient, sda_patient_numbers)
    import_aliases(patient, sda_names)
    import_addresses(patient, sda_addresses)
    import_medications(patient, sda_medications)
    import_results(patient, sda_lab_orders)

    db.session.commit()

    return True
