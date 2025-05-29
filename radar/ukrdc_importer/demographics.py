import logging

from cornflake.exceptions import ValidationError

from radar.database import db
from radar.models.demographics import Ethnicity
from radar.models.patient_demographics import PatientDemographics
from radar.ukrdc_importer.serializers import PatientSerializer
from radar.ukrdc_importer.utils import (
    get_import_group,
    get_import_user,
)
from radar.utils import get_path


logger = logging.getLogger(__name__)


class SDAPatient(object):
    MALE = ['1', 'M', 'MALE']
    FEMALE = ['2', 'F', 'FEMALE']
    ETHNICITY = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'Z']
    ETHNICITY_DESCRIPTIONS = {
        'WHITE - BRITISH': 'A',
        'WHITE - IRISH': 'B',
        'OTHER WHITE BACKGROUND': 'C',
        'MIXED - WHITE AND BLACK CARIBBEAN': 'D',
        'MIXED - WHITE AND BLACK AFRICAN': 'E',
        'MIXED - WHITE AND ASIAN': 'F',
        'OTHER MIXED BACKGROUND': 'G',
        'ASIAN OR ASIAN BRITISH - INDIAN': 'H',
        'ASIAN OR ASIAN BRITISH - PAKISTANI': 'J',
        'ASIAN OR ASIAN BRITISH - BANGLADESHI': 'K',
        'OTHER ASIAN BACKGROUND': 'L',
        'BLACK CARRIBEAN': 'M',
        'BLACK AFRICAN': 'N',
        'OTHER BLACK BACKGROUND': 'P',
        'CHINESE': 'R',
        'OTHER ETHNIC BACKGROUND': 'S',
        'REFUSED / NOT STATED': 'Z',
    }

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
        else:
            description = get_path(self.data, 'ethnic_group', 'description')
            if description is not None:
                description = description.strip().upper()
                return self.ETHNICITY_DESCRIPTIONS.get(description)

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


def parse_demographics(sda_patient,adapter):
    serializer = PatientSerializer()
    try:
        sda_patient = serializer.run_validation(sda_patient)
    except ValidationError as e:
        adapter.error('Ignoring invalid patient errors={errors}'.format(errors=e.flatten()))
        return None

    sda_patient = SDAPatient(sda_patient)

    return sda_patient


def get_demographics(patient):
    q = PatientDemographics.query
    q = q.filter(PatientDemographics.source_group == get_import_group())
    q = q.filter(PatientDemographics.source_type == 'UKRDC')
    q = q.filter(PatientDemographics.patient == patient)
    return q.first()


def get_ethnicity(code):
    return Ethnicity.query.filter_by(code=code).first()


def convert_demographics(patient, sda_patient):
    source_group = get_import_group()
    user = get_import_user()

    demographics = get_demographics(patient)

    if demographics is None:
        logger.info('Creating demographics')
        demographics = PatientDemographics()
    else:
        logger.info('Updating demographics id={id}'.format(id=demographics.id))

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
    demographics.ethnicity = get_ethnicity(sda_patient.ethnic_group)
    demographics.home_number = sda_patient.home_phone_number
    demographics.work_number = sda_patient.work_phone_number
    demographics.mobile_number = sda_patient.mobile_phone_number
    demographics.email_address = sda_patient.email_address

    db.session.add(demographics)

    return demographics


def import_demographics(patient, sda_patient,adapter):
    adapter.info('Importing demographics: %s', patient.id)

    sda_patient = parse_demographics(sda_patient,adapter)

    if sda_patient:
        convert_demographics(patient, sda_patient)
        n = 1
    else:
        n = 0

    logger.info('Imported {n} demographics record(s)'.format(n=n))
