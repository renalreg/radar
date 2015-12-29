from datetime import date, datetime, timedelta

import pytest
import pytz

from radar.models import PatientDemographics, Patient, DataSource, GENDER_MALE, GENDER_FEMALE
from radar.validation.core import ValidationError
from radar.validation.patient_demographics import PatientDemographicsValidation
from radar.validation.validators import DAY_ZERO
from radar.tests.validation.helpers import validation_runner


@pytest.fixture
def patient():
    patient = Patient()
    return patient


@pytest.fixture
def demographics(patient):
    obj = PatientDemographics()
    obj.data_source = DataSource()
    obj.patient = patient
    obj.first_name = 'JOHN'
    obj.last_name = 'SMITH'
    obj.date_of_birth = date(1900, 1, 1)
    obj.date_of_death = date(2000, 1, 1)
    obj.gender = GENDER_MALE
    obj.ethnicity = 'A'
    obj.home_number = '111111'
    obj.work_number = '222222'
    obj.mobile_number = '333333'
    obj.email_address = 'foo@example.org'
    return obj


def test_valid(demographics):
    obj = valid(demographics)
    assert obj.first_name == 'JOHN'
    assert obj.last_name == 'SMITH'
    assert obj.date_of_birth == date(1900, 1, 1)
    assert obj.date_of_death == date(2000, 1, 1)
    assert obj.gender == GENDER_MALE
    assert obj.ethnicity == 'A'
    assert obj.home_number == '111111'
    assert obj.work_number == '222222'
    assert obj.mobile_number == '333333'
    assert obj.email_address == 'foo@example.org'
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_missing(demographics):
    demographics.patient = None
    invalid(demographics)


def test_data_source_missing(demographics):
    demographics.data_source = None
    invalid(demographics)


def test_first_name_blank(demographics):
    demographics.first_name = ''
    invalid(demographics)


def test_first_name_missing(demographics):
    demographics.first_name = None
    invalid(demographics)


def test_first_name_extra_spaces(demographics):
    demographics.first_name = 'FOO   BAR'
    obj = valid(demographics)
    assert obj.first_name == 'FOO BAR'


def test_first_name_to_upper(demographics):
    demographics.first_name = 'foo'
    obj = valid(demographics)
    assert obj.first_name == 'FOO'


def test_last_name_blank(demographics):
    demographics.last_name = ''
    invalid(demographics)


def test_last_name_missing(demographics):
    demographics.last_name = None
    invalid(demographics)


def test_last_name_extra_spaces(demographics):
    demographics.last_name = 'FOO   BAR'
    obj = valid(demographics)
    assert obj.last_name == 'FOO BAR'


def test_last_name_to_upper(demographics):
    demographics.last_name = 'foo'
    obj = valid(demographics)
    assert obj.last_name == 'FOO'


def test_date_of_birth_missing(demographics):
    demographics.date_of_birth = None
    invalid(demographics)


def test_date_of_birth_in_future(demographics):
    tomorrow = datetime.now(pytz.utc) + timedelta(days=1)
    demographics.date_of_birth = tomorrow
    demographics.date_of_death = tomorrow
    invalid(demographics)


def test_date_of_birth_before_day_zero(demographics):
    demographics.date_of_birth = DAY_ZERO - timedelta(days=1)
    invalid(demographics)


def test_date_of_death_missing(demographics):
    demographics.date_of_death = None
    valid(demographics)


def test_date_of_death_in_future(demographics):
    tomorrow = datetime.now(pytz.utc) + timedelta(days=1)
    demographics.date_of_death = tomorrow
    invalid(demographics)


def test_date_of_death_before_date_of_birth(demographics):
    demographics.date_of_death = demographics.date_of_birth - timedelta(days=1)
    invalid(demographics)


def test_date_of_death_on_date_of_birth(demographics):
    demographics.date_of_death = demographics.date_of_birth
    valid(demographics)


def test_gender_male(demographics):
    demographics.gender = GENDER_MALE
    obj = valid(demographics)
    assert obj.gender == GENDER_MALE


def test_gender_female(demographics):
    demographics.gender = GENDER_FEMALE
    obj = valid(demographics)
    assert obj.gender == GENDER_FEMALE


def test_gender_blank(demographics):
    demographics.gender = ''
    invalid(demographics)


def test_gender_missing(demographics):
    demographics.gender = None
    invalid(demographics)


def test_gender_invalid(demographics):
    demographics.gender = 'X'
    invalid(demographics)


def test_ethnicity_missing(demographics):
    demographics.ethnicity = None
    obj = valid(demographics)
    obj.ethnicity = None


def test_home_number_blank(demographics):
    demographics.home_number = ''
    obj = valid(demographics)
    assert obj.home_number is None


def test_home_number_missing(demographics):
    demographics.home_number = None
    obj = valid(demographics)
    assert obj.home_number is None


def test_home_number_extra_spaces(demographics):
    demographics.home_number = '12345   12345'
    obj = valid(demographics)
    assert obj.home_number == '12345 12345'


def test_work_number_blank(demographics):
    demographics.work_number = ''
    obj = valid(demographics)
    assert obj.work_number is None


def test_work_number_missing(demographics):
    demographics.work_number = None
    obj = valid(demographics)
    assert obj.work_number is None


def test_work_number_extra_spaces(demographics):
    demographics.work_number = '12345   12345'
    obj = valid(demographics)
    assert obj.work_number == '12345 12345'


def test_mobile_number_blank(demographics):
    demographics.mobile_number = ''
    obj = valid(demographics)
    assert obj.mobile_number is None


def test_mobile_number_missing(demographics):
    demographics.mobile_number = None
    obj = valid(demographics)
    assert obj.mobile_number is None


def test_mobile_number_extra_spaces(demographics):
    demographics.mobile_number = '12345   12345'
    obj = valid(demographics)
    assert obj.mobile_number == '12345 12345'


def test_email_address_blank(demographics):
    demographics.email_address = ''
    obj = valid(demographics)
    assert obj.email_address is None


def test_email_address_missing(demographics):
    demographics.email_address = None
    obj = valid(demographics)
    assert obj.email_address is None


def test_email_address_invalid(demographics):
    demographics.email_address = 'HELLO'
    invalid(demographics)


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(PatientDemographics, PatientDemographicsValidation, obj, **kwargs)
