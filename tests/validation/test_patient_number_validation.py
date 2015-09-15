import pytest
from radar.lib.models import DataSource, PatientNumber, ORGANISATION_TYPE_OTHER, Patient, User, \
    Organisation, ORGANISATION_CODE_NHS, ORGANISATION_CODE_CHI, ORGANISATION_CODE_HANDC, ORGANISATION_CODE_RADAR, \
    ORGANISATION_CODE_UKRR
from radar.lib.validation.core import ValidationError
from radar.lib.validation.patient_numbers import PatientNumberValidation


@pytest.fixture
def patient():
    patient = Patient()
    return patient


@pytest.fixture
def number(patient):
    obj = PatientNumber()
    obj.data_source = DataSource()
    obj.patient = patient
    obj.organisation = Organisation(code='FOO', type=ORGANISATION_TYPE_OTHER)
    obj.number = '123'
    return obj


def test_valid(number):
    organisation = number.organisation
    obj = valid(number)
    assert obj.organisation == organisation
    assert obj.number == '123'
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_missing(number):
    number.patient = None
    invalid(number)


def test_data_source_missing(number):
    number.data_source = None
    invalid(number)


def test_organisation_missing(number):
    number.organisation = None
    invalid(number)


def test_organisation_radar(number):
    number.organisation = Organisation(code=ORGANISATION_CODE_RADAR, type=ORGANISATION_TYPE_OTHER)
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
    number.organisation = Organisation(code=ORGANISATION_CODE_NHS, type=ORGANISATION_TYPE_OTHER)
    number.number = '9434765919'
    valid(number)


def test_nhs_no_invalid(number):
    number.organisation = Organisation(code=ORGANISATION_CODE_NHS, type=ORGANISATION_TYPE_OTHER)
    number.number = '9434765918'
    invalid(number)


def test_chi_no_valid(number):
    number.organisation = Organisation(code=ORGANISATION_CODE_CHI, type=ORGANISATION_TYPE_OTHER)
    number.number = '9434765919'
    valid(number)


def test_chi_no_invalid(number):
    number.organisation = Organisation(code=ORGANISATION_CODE_CHI, type=ORGANISATION_TYPE_OTHER)
    number.number = '9434765918'
    invalid(number)


def test_handc_no_valid(number):
    number.organisation = Organisation(code=ORGANISATION_CODE_HANDC, type=ORGANISATION_TYPE_OTHER)
    number.number = '9434765919'
    valid(number)


def test_handc_no_invalid(number):
    number.organisation = Organisation(code=ORGANISATION_CODE_HANDC, type=ORGANISATION_TYPE_OTHER)
    number.number = '9434765918'
    invalid(number)


def test_ukrr_no_valid(number):
    number.organisation = Organisation(code=ORGANISATION_CODE_UKRR, type=ORGANISATION_TYPE_OTHER)
    number.number = '200012345'
    valid(number)


def test_ukrr_no_invalid(number):
    number.organisation = Organisation(code=ORGANISATION_CODE_UKRR, type=ORGANISATION_TYPE_OTHER)
    number.number = '2000123456'
    invalid(number)


def valid(obj):
    return validate(obj)


def invalid(obj):
    with pytest.raises(ValidationError) as e:
        validate(obj)

    return e


def validate(obj):
    validation = PatientNumberValidation()
    ctx = {'user': User(is_admin=True)}
    validation.before_update(ctx, PatientNumber())
    old_obj = validation.clone(obj)
    obj = validation.after_update(ctx, old_obj, obj)
    return obj
