from datetime import date, timedelta

import pytest

from radar.models import Patient, PatientDemographics, DataSource
from radar.models.patient_addresses import PatientAddress
from radar.validation.core import ValidationError
from radar.validation.patient_addresses import PatientAddressValidation
from radar.tests.validation.helpers import validation_runner


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def address(patient):
    obj = PatientAddress()
    obj.data_source = DataSource()
    obj.patient = patient
    obj.from_date = date(2014, 1, 1)
    obj.to_date = date(2015, 1, 1)
    obj.address_line_1 = 'Learning and Research Building'
    obj.address_line_2 = 'Southmead Hospital'
    obj.address_line_3 = 'Bristol'
    obj.postcode = 'BS10 5NB'
    return obj


def test_valid(address):
    obj = valid(address)
    assert obj.from_date == date(2014, 1, 1)
    assert obj.to_date == date(2015, 1, 1)
    assert obj.address_line_1 == 'Learning and Research Building'
    assert obj.address_line_2 == 'Southmead Hospital'
    assert obj.address_line_3 == 'Bristol'
    assert obj.postcode == 'BS10 5NB'
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_missing(address):
    address.patient = None
    invalid(address)


def test_data_source_missing(address):
    address.data_source = None
    invalid(address)


def test_from_date_missing(address):
    address.from_date = None
    valid(address)


def test_from_date_before_dob(address):
    address.from_date = date(1999, 1, 1)
    invalid(address)


def test_to_date_missing(address):
    address.to_date = None
    valid(address)


def test_to_date_before_dob(address):
    address.from_date = date(1999, 1, 1)
    address.to_date = date(1999, 1, 2)
    invalid(address)


def test_to_date_before_from_date(address):
    address.to_date = address.from_date - timedelta(days=1)
    invalid(address)


def test_address_line_1_blank(address):
    address.address_line_1 = ''
    invalid(address)


def test_address_line_1_missing(address):
    address.address_line_1 = None
    invalid(address)


def test_address_line_1_comma(address):
    address.address_line_1 = ','
    invalid(address)


def test_address_line_1_extra_spaces(address):
    address.address_line_1 = 'foo   bar'
    valid(address)
    assert address.address_line_1 == 'foo bar'


def test_address_line_2_blank(address):
    address.address_line_2 = ''
    obj = valid(address)
    assert obj.address_line_2 is None


def test_address_line_2_missing(address):
    address.address_line_2 = None
    valid(address)


def test_address_line_2_comma(address):
    address.address_line_2 = ','
    valid(address)
    assert address.address_line_2 is None


def test_address_line_2_extra_spaces(address):
    address.address_line_2 = 'foo   bar'
    valid(address)
    assert address.address_line_2 == 'foo bar'


def test_address_line_3_blank(address):
    address.address_line_3 = ''
    obj = valid(address)
    assert obj.address_line_3 is None


def test_address_line_3_missing(address):
    address.address_line_3 = None
    valid(address)


def test_address_line_3_comma(address):
    address.address_line_3 = ','
    valid(address)
    assert address.address_line_3 is None


def test_address_line_3_extra_spaces(address):
    address.address_line_3 = 'foo   bar'
    valid(address)
    assert address.address_line_3 == 'foo bar'


def test_postcode_blank(address):
    address.postcode = ''
    invalid(address)


def test_postcode_none(address):
    address.postcode = None
    invalid(address)


def test_postcode_invalid(address):
    address.postcode = 'HELLO'
    invalid(address)


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(PatientAddress, PatientAddressValidation, obj, **kwargs)
