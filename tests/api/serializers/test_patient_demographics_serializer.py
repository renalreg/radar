from datetime import date, timedelta

from cornflake.exceptions import ValidationError
import pytest

from radar.api.serializers.patient_demographics import PatientDemographicsSerializer
from radar.api.serializers.validators import DAY_ZERO
from radar.models.demographics import Ethnicity, Nationality
from radar.models.groups import Group
from radar.models.patient_codes import GENDER_MALE, GENDER_FEMALE
from radar.models.patients import Patient
from radar.models.source_types import SOURCE_TYPE_MANUAL
from radar.models.users import User


@pytest.fixture
def patient():
    patient = Patient()
    return patient


@pytest.fixture
def demographics(patient):
    return {
        'source_group': Group(),
        'source_type': SOURCE_TYPE_MANUAL,
        'patient': patient,
        'first_name': 'JOHN',
        'last_name': 'SMITH',
        'date_of_birth': date(1900, 1, 1),
        'date_of_death': date(2000, 1, 1),
        'gender': GENDER_MALE,
        'home_number': '111111',
        'work_number': '222222',
        'mobile_number': '333333',
        'email_address': 'foo@example.org',
        'nationality': Nationality(),
        'ethnicity': Ethnicity(),
    }


def test_valid(demographics):
    obj = valid(demographics)
    assert obj.first_name == 'JOHN'
    assert obj.last_name == 'SMITH'
    assert obj.date_of_birth == date(1900, 1, 1)
    assert obj.date_of_death == date(2000, 1, 1)
    assert obj.gender == GENDER_MALE
    assert obj.home_number == '111111'
    assert obj.work_number == '222222'
    assert obj.mobile_number == '333333'
    assert obj.email_address == 'foo@example.org'
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_none(demographics):
    demographics['patient'] = None
    invalid(demographics)


def test_source_group_none(demographics):
    demographics['source_group'] = None
    invalid(demographics)


def test_source_type_none(demographics):
    demographics['source_type'] = None
    demographics = valid(demographics)
    assert demographics.source_type == SOURCE_TYPE_MANUAL


def test_first_name_blank(demographics):
    demographics['first_name'] = ''
    invalid(demographics)


def test_first_name_none(demographics):
    demographics['first_name'] = None
    invalid(demographics)


def test_first_name_extra_spaces(demographics):
    demographics['first_name'] = 'FOO   BAR'
    obj = valid(demographics)
    assert obj.first_name == 'FOO BAR'


def test_first_name_to_upper(demographics):
    demographics['first_name'] = 'foo'
    obj = valid(demographics)
    assert obj.first_name == 'FOO'


def test_last_name_blank(demographics):
    demographics['last_name'] = ''
    invalid(demographics)


def test_last_name_none(demographics):
    demographics['last_name'] = None
    invalid(demographics)


def test_last_name_extra_spaces(demographics):
    demographics['last_name'] = 'FOO   BAR'
    obj = valid(demographics)
    assert obj.last_name == 'FOO BAR'


def test_last_name_to_upper(demographics):
    demographics['last_name'] = 'foo'
    obj = valid(demographics)
    assert obj.last_name == 'FOO'


def test_date_of_birth_none(demographics):
    demographics['date_of_birth'] = None
    invalid(demographics)


def test_date_of_birth_in_future(demographics):
    tomorrow = date.today() + timedelta(days=1)
    demographics['date_of_birth'] = tomorrow
    demographics['date_of_death'] = tomorrow
    invalid(demographics)


def test_date_of_birth_before_day_zero(demographics):
    demographics['date_of_birth'] = DAY_ZERO - timedelta(days=1)
    invalid(demographics)


def test_date_of_death_none(demographics):
    demographics['date_of_death'] = None
    valid(demographics)


def test_date_of_death_in_future(demographics):
    tomorrow = date.today() + timedelta(days=1)
    demographics['date_of_death'] = tomorrow
    invalid(demographics)


def test_date_of_death_before_date_of_birth(demographics):
    demographics['date_of_death'] = demographics['date_of_birth'] - timedelta(days=1)
    invalid(demographics)


def test_date_of_death_on_date_of_birth(demographics):
    demographics['date_of_death'] = demographics['date_of_birth']
    valid(demographics)


def test_gender_male(demographics):
    demographics['gender'] = GENDER_MALE
    obj = valid(demographics)
    assert obj.gender == GENDER_MALE


def test_gender_female(demographics):
    demographics['gender'] = GENDER_FEMALE
    obj = valid(demographics)
    assert obj.gender == GENDER_FEMALE


def test_gender_blank(demographics):
    demographics['gender'] = ''
    invalid(demographics)


def test_gender_none(demographics):
    demographics['gender'] = None
    invalid(demographics)


def test_gender_invalid(demographics):
    demographics['gender'] = 'X'
    invalid(demographics)


def test_ethnicity_none(demographics):
    demographics['ethnicity'] = None
    obj = valid(demographics)
    obj.ethnicity = None


def test_home_number_blank(demographics):
    demographics['home_number'] = ''
    obj = valid(demographics)
    assert obj.home_number is None


def test_home_number_none(demographics):
    demographics['home_number'] = None
    obj = valid(demographics)
    assert obj.home_number is None


def test_home_number_extra_spaces(demographics):
    demographics['home_number'] = '12345   12345'
    obj = valid(demographics)
    assert obj.home_number == '12345 12345'


def test_work_number_blank(demographics):
    demographics['work_number'] = ''
    obj = valid(demographics)
    assert obj.work_number is None


def test_work_number_none(demographics):
    demographics['work_number'] = None
    obj = valid(demographics)
    assert obj.work_number is None


def test_work_number_extra_spaces(demographics):
    demographics['work_number'] = '12345   12345'
    obj = valid(demographics)
    assert obj.work_number == '12345 12345'


def test_mobile_number_blank(demographics):
    demographics['mobile_number'] = ''
    obj = valid(demographics)
    assert obj.mobile_number is None


def test_mobile_number_none(demographics):
    demographics['mobile_number'] = None
    obj = valid(demographics)
    assert obj.mobile_number is None


def test_mobile_number_extra_spaces(demographics):
    demographics['mobile_number'] = '12345   12345'
    obj = valid(demographics)
    assert obj.mobile_number == '12345 12345'


def test_email_address_blank(demographics):
    demographics['email_address'] = ''
    obj = valid(demographics)
    assert obj.email_address is None


def test_email_address_none(demographics):
    demographics['email_address'] = None
    obj = valid(demographics)
    assert obj.email_address is None


def test_email_address_invalid(demographics):
    demographics['email_address'] = 'HELLO'
    invalid(demographics)


def invalid(data):
    with pytest.raises(ValidationError) as e:
        valid(data)

    return e


def valid(data):
    serializer = PatientDemographicsSerializer(data=data, context={'user': User(is_admin=True)})
    serializer.is_valid(raise_exception=True)
    return serializer.save()
