import logging

from jsonschema import ValidationError

from radar.models.patient_demographics import PatientDemographics
from radar.database import db

from radar_ukrdc_importer.utils import (
    load_validator,
    delete_list,
    build_id,
    get_path,
    parse_datetime_path,
    get_import_user,
    get_import_group
)


logger = logging.getLogger(__name__)


class SDAPatient(object):
    MALE = ['0', 'M', 'MALE']
    FEMALE = ['1', 'F', 'FEMALE']
    ETHNICITY = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'Z']

    def __init__(self, data):
        self.data = data

    @property
    def given_name(self):
        return get_path(self.data, 'name', 'given_name')

    @property
    def family_name(self):
        return get_path(self.data, 'name', 'family_name')

    @property
    def birth_time(self):
        return self.data.get('birth_time')

    @property
    def birth_date(self):
        birth_time = self.birth_time

        if birth_time is None:
            return None
        else:
            return birth_time.date()

    @property
    def death_time(self):
        return self.data.get('death_time')

    @property
    def death_date(self):
        death_time = self.death_time

        if death_time is None:
            return None
        else:
            return death_time.date()

    @property
    def gender(self):
        gender = get_path(self.data, 'gender', 'code')

        if gender is not None:
            gender = gender.upper()

            if gender in self.MALE:
                return 1
            elif gender in self.FEMALE:
                return 2

        return None

    @property
    def ethnic_group(self):
        ethnicity = get_path(self.data, 'ethnic_group', 'code')

        if ethnicity is not None:
            ethnicity = ethnicity.upper()

            if ethnicity in self.ETHNICITY:
                return ethnicity

        return None

    @property
    def home_phone_number(self):
        return get_path(self.data, 'contact_info', 'home_phone_number')

    @property
    def work_phone_number(self):
        return get_path(self.data, 'contact_info', 'work_phone_number')

    @property
    def mobile_phone_number(self):
        return get_path(self.data, 'contact_info', 'mobile_phone_number')

    @property
    def email_address(self):
        return get_path(self.data, 'contact_info', 'email_address')


def parse_demographics(sda_patient):
    validator = load_validator('patient.json')

    try:
        validator.validate(sda_patient)
    except ValidationError as e:
        print e
        logger.error('Ignoring invalid patient')
        return None

    for key in ['birth_time', 'death_time']:
        parse_datetime_path(sda_patient, key)

    sda_patient = SDAPatient(sda_patient)

    return sda_patient


def get_demographics(demographics_id):
    return PatientDemographics.query.get(demographics_id)


def get_demographics_list(patient):
    q = PatientDemographics.query
    q = q.filter(PatientDemographics.source_type == 'UKRDC')
    q = q.filter(PatientDemographics.patient == patient)
    return q.all()


def sync_demographics(patient, demographics_to_keep):
    def log(demographics):
        logger.info('Deleting demographics id={}'.format(demographics.id))

    demographics_list = get_demographics_list(patient)
    delete_list(demographics_list, [demographics_to_keep], delete_f=log)


def build_demographics_id(patient, sda_patient):
    return build_id(patient.id, PatientDemographics.__tablename__)


def convert_demographics(patient, sda_patient):
    source_group = get_import_group()
    user = get_import_user()

    demographics_id = build_demographics_id(patient, sda_patient)
    demographics = get_demographics(demographics_id)

    if demographics is None:
        logger.info('Creating demographics id={id}'.format(id=demographics_id))
        demographics = PatientDemographics(id=demographics_id)
    else:
        logger.info('Updating demographics id={id}'.format(id=demographics_id))

    demographics.patient = patient
    demographics.source_group = source_group
    demographics.source_type = 'UKRDC'
    demographics.created_user = user
    demographics.modified_user = user

    demographics.first_name = sda_patient.given_name
    demographics.last_name = sda_patient.family_name
    demographics.date_of_birth = sda_patient.birth_date
    demographics.date_of_death = sda_patient.death_date
    demographics.gender = sda_patient.gender
    demographics.ethnicity = sda_patient.ethnic_group
    demographics.home_number = sda_patient.home_phone_number
    demographics.work_number = sda_patient.work_phone_number
    demographics.mobile_number = sda_patient.mobile_phone_number
    demographics.email_address = sda_patient.email_address

    db.session.add(demographics)

    return demographics


def import_demographics(patient, sda_patient):
    logger.info('Importing demographics')

    sda_patient = parse_demographics(sda_patient)

    if sda_patient:
        demographics = convert_demographics(patient, sda_patient)
        sync_demographics(patient, demographics)
        n = 1
    else:
        n = 0

    logger.info('Imported {n} demographics record(s)'.format(n=n))
