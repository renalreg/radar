import pytest

from radar.models.patient_numbers import PatientNumber
from radar.models.patients import Patient
from radar.models.groups import Group, GROUP_TYPE, GROUP_CODE_NHS,\
    GROUP_CODE_CHI, GROUP_CODE_HANDC, GROUP_CODE_RADAR, GROUP_CODE_UKRR
from radar.models.source_types import SOURCE_TYPE_RADAR
from radar.validation.core import ValidationError
from radar.validation.patient_numbers import PatientNumberValidation
from radar.tests.validation.helpers import validation_runner


@pytest.fixture
def patient():
    patient = Patient()
    return patient


@pytest.fixture
def number(patient):
    obj = PatientNumber()
    obj.source_group = Group()
    obj.source_type = SOURCE_TYPE_RADAR
    obj.patient = patient
    obj.number_group = Group(code='FOO', type=GROUP_TYPE.OTHER)
    obj.number = '123'
    return obj


def test_valid(number):
    number_group = number.number_group
    obj = valid(number)
    assert obj.number_group == number_group
    assert obj.number == '123'
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_missing(number):
    number.patient = None
    invalid(number)


def test_source_group_missing(number):
    number.source_group = None
    invalid(number)


def test_source_type_missing(number):
    number.source_type = None
    number = valid(number)
    assert number.source_type == 'RADAR'


def test_number_group_missing(number):
    number.number_group = None
    invalid(number)


def test_number_group_radar(number):
    number.number_group = Group(code=GROUP_CODE_RADAR, type=GROUP_TYPE.OTHER)
    invalid(number)


def test_number_missing(number):
    number.number = None
    invalid(number)


def test_number_blank(number):
    number.number = ''
    invalid(number)


def test_number_remove_extra_spaces(number):
    number.number = '123   456'
    obj = valid(number)
    assert obj.number == '123 456'


def test_nhs_no_valid(number):
    number.number_group = Group(code=GROUP_CODE_NHS, type=GROUP_TYPE.OTHER)
    number.number = '9434765919'
    valid(number)


def test_nhs_no_invalid(number):
    number.number_group = Group(code=GROUP_CODE_NHS, type=GROUP_TYPE.OTHER)
    number.number = '9434765918'
    invalid(number)


def test_chi_no_valid(number):
    number.number_group = Group(code=GROUP_CODE_CHI, type=GROUP_TYPE.OTHER)
    number.number = '101299877'
    valid(number)


def test_chi_no_invalid(number):
    number.number_group = Group(code=GROUP_CODE_CHI, type=GROUP_TYPE.OTHER)
    number.number = '9434765918'
    invalid(number)


def test_handc_no_valid(number):
    number.number_group = Group(code=GROUP_CODE_HANDC, type=GROUP_TYPE.OTHER)
    number.number = '3232255825'
    valid(number)


def test_handc_no_invalid(number):
    number.number_group = Group(code=GROUP_CODE_HANDC, type=GROUP_TYPE.OTHER)
    number.number = '9434765918'
    invalid(number)


def test_ukrr_no_valid(number):
    number.number_group = Group(code=GROUP_CODE_UKRR, type=GROUP_TYPE.OTHER)
    number.number = '200012345'
    valid(number)


def test_ukrr_no_invalid(number):
    number.number_group = Group(code=GROUP_CODE_UKRR, type=GROUP_TYPE.OTHER)
    number.number = '2000123456'
    invalid(number)


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(PatientNumber, PatientNumberValidation, obj, **kwargs)
