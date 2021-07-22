import logging

from radar.database import db
from radar.models.groups import GROUP_TYPE
from radar.models.patient_numbers import PatientNumber
from radar.ukrdc_importer.serializers import PatientNumberSerializer
from radar.ukrdc_importer.utils import (
    build_id,
    delete_list,
    get_group,
    get_import_group,
    get_import_user,
    unique_list,
    validate_list,
)


logger = logging.getLogger(__name__)


class SDAPatientNumber(object):
    def __init__(self, data):
        self.data = data

    @property
    def number(self):
        return self.data['number']

    @property
    def number_type(self):
        return self.data['number_type']

    @property
    def organization(self):
        return self.data['organization']['code']


def parse_patient_numbers(sda_patient_numbers):
    def log(index, sda_medication, e):
        logger.error(
            'Ignoring invalid patient number index={index}, errors={errors}'.format(
                index=index,
                errors=e.flatten()
            )
        )

    serializer = PatientNumberSerializer()
    sda_patient_numbers = validate_list(sda_patient_numbers, serializer, invalid_f=log)
    sda_patient_numbers = map(SDAPatientNumber, sda_patient_numbers)

    return sda_patient_numbers


def unique_patient_numbers(sda_patient_numbers):
    def key(sda_patient_number):
        return sda_patient_number.organization

    def log(sda_patient_number):
        logger.warning('Ignoring duplicate patient number')

    sda_patient_numbers = unique_list(sda_patient_numbers, key_f=key, duplicate_f=None)

    return sda_patient_numbers


def get_patient_number(patient_number_id):
    return PatientNumber.query.get(patient_number_id)


def get_patient_numbers(patient):
    q = PatientNumber.query
    q = q.filter(PatientNumber.source_type == 'UKRDC')
    q = q.filter(PatientNumber.patient == patient)
    return q.all()


def sync_patient_numbers(patient, patient_numbers_to_keep):
    def log(patient_number):
        logger.info('Deleting patient number id={}'.format(patient_number.id))

    patient_numbers = get_patient_numbers(patient)
    delete_list(patient_numbers, patient_numbers_to_keep, delete_f=log)


def build_patient_number_id(patient, sda_patient_number):
    return build_id(patient.id, PatientNumber.__tablename__, sda_patient_number.organization)


def convert_patient_numbers(patient, sda_patient_numbers):
    source_group = get_import_group()
    user = get_import_user()

    patient_numbers = list()

    for sda_patient_number in sda_patient_numbers:
        code = sda_patient_number.organization

        number_group = get_group(code)

        if number_group is None:
            logger.error('Ignoring patient number due to unknown organization code={code}'.format(code=code))
            continue

        # Ignore patient numbers for system groups
        if number_group.type == GROUP_TYPE.SYSTEM:
            continue

        patient_number_id = build_patient_number_id(patient, sda_patient_number)
        patient_number = get_patient_number(patient_number_id)

        if patient_number is None:
            logger.info('Creating patient number id={id}'.format(id=patient_number_id))
            patient_number = PatientNumber(id=patient_number_id)
        else:
            logger.info('Updating patient number id={id}'.format(id=patient_number_id))

        patient_number.patient = patient
        patient_number.source_group = source_group
        patient_number.source_type = 'UKRDC'
        patient_number.created_user = user
        patient_number.modified_user = user

        patient_number.number = sda_patient_number.number
        patient_number.number_group = number_group

        db.session.add(patient_number)
        patient_numbers.append(patient_number)

    return patient_numbers


def import_patient_numbers(patient, sda_patient_numbers):
    logger.info('Importing patient numbers')

    sda_patient_numbers = parse_patient_numbers(sda_patient_numbers)
    sda_patient_numbers = unique_patient_numbers(sda_patient_numbers)
    patient_numbers = convert_patient_numbers(patient, sda_patient_numbers)
    sync_patient_numbers(patient, patient_numbers)

    logger.info('Imported {n} patient number(s)'.format(n=len(patient_numbers)))
