from datetime import date, datetime, timedelta
import pytest
import pytz
from radar.lib.models import PatientDemographics, Patient, DataSource, User, EthnicityCode
from radar.lib.validation.core import ValidationError
from radar.lib.validation.patient_demographics import PatientDemographicsValidation
from radar.lib.validation.validators import DAY_ZERO


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
    obj.gender = 'M'
    obj.ethnicity_code = EthnicityCode(id=1)
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
    assert obj.gender == 'M'
    assert obj.ethnicity_code == demographics.ethnicity_code
    assert obj.home_number == '111111'
    assert obj.work_number == '222222'
    assert obj.mobile_number == '333333'
    assert obj.email_address == 'foo@example.org'


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
    tomorrow = datetime.now(pytz.UTC) + timedelta(days=1)
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
    tomorrow = datetime.now(pytz.UTC) + timedelta(days=1)
    demographics.date_of_death = tomorrow
    invalid(demographics)


def test_date_of_death_before_date_of_birth(demographics):
    demographics.date_of_death = demographics.date_of_birth - timedelta(days=1)
    invalid(demographics)


def test_date_of_death_on_date_of_birth(demographics):
    demographics.date_of_death = demographics.date_of_birth
    valid(demographics)


def test_gender_m_lower(demographics):
    demographics.gender = 'm'
    obj = valid(demographics)
    assert obj.gender == 'M'


def test_gender_f_lower(demographics):
    demographics.gender = 'f'
    obj = valid(demographics)
    assert obj.gender == 'F'


def test_gender_m_upper(demographics):
    demographics.gender = 'M'
    obj = valid(demographics)
    assert obj.gender == 'M'


def test_gender_f_upper(demographics):
    demographics.gender = 'F'
    obj = valid(demographics)
    assert obj.gender == 'F'


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
    demographics.ethnicity_code = None
    invalid(demographics)


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


def valid(obj):
    return validate(obj)


def invalid(obj):
    with pytest.raises(ValidationError) as e:
        validate(obj)

    return e


def validate(obj):
    validation = PatientDemographicsValidation()
    ctx = {'user': User(is_admin=True)}
    validation.before_update(ctx, PatientDemographics())
    old_obj = validation.clone(obj)
    obj = validation.after_update(ctx, old_obj, obj)
    return obj
