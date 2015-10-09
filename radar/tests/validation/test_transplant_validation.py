from datetime import date, timedelta

import pytest

from radar.lib.models import Patient, PatientDemographics, Transplant, DataSource
from radar.lib.validation.core import ValidationError
from radar.lib.validation.transplants import TransplantValidation
from utils import validation_runner


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def transplant(patient):
    obj = Transplant()
    obj.data_source = DataSource()
    obj.patient = patient
    obj.transplant_date = date(2015, 1, 1)
    obj.transplant_type = 'LIVE'
    obj.date_failed = date(2015, 1, 2)
    return obj


def test_valid(transplant):
    obj = valid(transplant)
    assert obj.transplant_date == date(2015, 1, 1)
    assert obj.transplant_type == 'LIVE'
    assert obj.date_failed == date(2015, 1, 2)
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_missing(transplant):
    transplant.patient = None
    invalid(transplant)


def test_data_source_missing(transplant):
    transplant.data_source = None
    invalid(transplant)


def test_transplant_date_missing(transplant):
    transplant.transplant_date = None
    invalid(transplant)


def test_transplant_date_before_dob(transplant):
    transplant.transplant_date = date(1999, 1, 1)
    invalid(transplant)


def test_transplant_date_future(transplant):
    transplant.transplant_date = date.today() + timedelta(days=1)
    invalid(transplant)


def test_transplant_type_missing(transplant):
    transplant.transplant_type = None
    invalid(transplant)


def test_transplant_type_invalid(transplant):
    transplant.transplant_type = 'FOO'
    invalid(transplant)


def test_date_failed_missing(transplant):
    transplant.date_failed = None
    valid(transplant)


def test_date_failed_before_dob(transplant):
    transplant.date_failed = date(1999, 1, 1)
    invalid(transplant)


def test_date_failed_future(transplant):
    transplant.date_failed = date.today() + timedelta(days=1)
    invalid(transplant)


def test_date_failed_before_transplant_date(transplant):
    transplant.date_failed = transplant.transplant_date - timedelta(days=1)
    invalid(transplant)


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(Transplant, TransplantValidation, obj, **kwargs)
