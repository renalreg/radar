import logging

from radar.models.medications import Medication
from radar.database import db
from radar.groups import is_radar_group

from radar_ukrdc.utils import (
    load_validator,
    validate_list,
    unique_list,
    parse_datetime_path,
    delete_list,
    build_id,
    get_path,
    get_import_user,
    get_group
)


logger = logging.getLogger(__name__)


class SDAMedication(object):
    def __init__(self, data):
        self.data = data

    @property
    def external_id(self):
        return self.data['external_id']

    @property
    def from_time(self):
        return self.data['from_time']

    @property
    def from_date(self):
        return self.from_time.date()

    @property
    def to_time(self):
        return self.data.get('to_time')

    @property
    def to_date(self):
        to_time = self.to_time

        if to_time is None:
            return None
        else:
            return to_time.date()

    @property
    def drug_product(self):
        return get_path(self.data, 'drug_product', 'product_name')

    @property
    def dose_u_o_m(self):
        return get_path(self.data, 'dose_u_o_m', 'code')

    @property
    def entering_organization(self):
        return get_path(self.data, 'entering_organization', 'code')


def parse_medications(sda_medications):
    def log(index, sda_medication, error):
        logger.error('Ignoring invalid medication index={index}'.format(index=index))

    validator = load_validator('medication.json')
    sda_medications = validate_list(sda_medications, validator, invalid_f=log)

    for sda_medication in sda_medications:
        parse_datetime_path(sda_medication, 'from_time')
        parse_datetime_path(sda_medication, 'to_time')

    sda_medications = map(SDAMedication, sda_medications)

    return sda_medications


def unique_medications(sda_medications):
    def key(sda_medication):
        return sda_medication.external_id

    def log(sda_medication):
        external_id = sda_medication.external_id
        logger.error('Ignoring duplicate medication external_id={external_id}'.format(external_id))

    sda_medications = unique_list(sda_medications, key_f=key, duplicate_f=log)

    return sda_medications


def preload_medications(patient):
    get_medications(patient)


def get_medication(medication_id):
    return Medication.query.get(medication_id)


def get_medications(patient):
    q = Medication.query
    q = q.filter(Medication.source_type == 'UKRDC')
    q = q.filter(Medication.patient == patient)
    return q.all()


def sync_medications(patient, medications_to_keep):
    def log(medication):
        logger.info('Deleting medication id={}'.format(medication.id))

    medications = get_medications(patient)
    delete_list(medications, medications_to_keep, delete_f=log)


def build_medication_id(patient, group, sda_medication):
    return build_id(patient.id, Medication.__tablename__, group.id, sda_medication.external_id)


def convert_medications(patient, sda_medications):
    user = get_import_user()

    medications = list()

    for sda_medication in sda_medications:
        code = sda_medication.entering_organization
        source_group = get_group(code)

        if source_group is None:
            logger.error('Ignoring medication due to unknown entering organization code={code}'.format(code=code))
            continue

        # Ignore RaDaR data
        if is_radar_group(source_group):
            continue

        medication_id = build_medication_id(patient, source_group, sda_medication)
        medication = get_medication(medication_id)

        if medication is None:
            logger.info('Creating medication id={id}'.format(id=medication_id))
            medication = Medication(id=medication_id)
        else:
            logger.info('Updating medication id={id}'.format(id=medication_id))

        medication.patient = patient
        medication.source_group = source_group
        medication.source_type = 'UKRDC'
        medication.created_user = user
        medication.modified_user = user

        medication.from_date = sda_medication.from_date
        medication.to_date = sda_medication.to_date
        medication.drug_text = sda_medication.drug_product
        medication.dose_text = sda_medication.dose_u_o_m

        db.session.add(medication)
        medications.append(medication)

    return medications


def import_medications(patient, sda_medications):
    logger.info('Importing medications')

    preload_medications(patient)

    sda_medications = parse_medications(sda_medications)
    sda_medications = unique_medications(sda_medications)
    medications = convert_medications(patient, sda_medications)
    sync_medications(patient, medications)

    logger.info('Imported {n} medication(s)'.format(n=len(medications)))
