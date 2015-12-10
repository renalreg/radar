from datetime import date, timedelta

import pytest

from radar.models import Dialysis, Patient, PatientDemographics, DataSource
from radar.validation.core import ValidationError
from radar.validation.dialysis import DialysisValidation
from radar.tests.validation.helpers import validation_runner


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def dialysis(patient):
    obj = Dialysis()
    obj.data_source = DataSource()
    obj.patient = patient
    obj.from_date = date(2015, 1, 1)
    obj.to_date = date(2015, 1, 2)
    obj.type_of_dialysis = 1
    return obj


def test_valid(dialysis):
    obj = valid(dialysis)
    assert obj.from_date == date(2015, 1, 1)
    assert obj.to_date == date(2015, 1, 2)
    assert obj.type_of_dialysis == 1
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_missing(dialysis):
    dialysis.patient = None
    invalid(dialysis)


def test_data_source_missing(dialysis):
    dialysis.data_source = None
    invalid(dialysis)


def test_from_date_missing(dialysis):
    dialysis.from_date = None
    invalid(dialysis)


def test_from_date_before_dob(dialysis):
    dialysis.from_date = date(1999, 1, 1)
    invalid(dialysis)


def test_from_date_future(dialysis):
    dialysis.from_date = date.today() + timedelta(days=1)
    invalid(dialysis)


def test_to_date_missing(dialysis):
    dialysis.to_date = None
    valid(dialysis)


def test_to_date_before_dob(dialysis):
    dialysis.to_date = date(1999, 1, 1)
    invalid(dialysis)


def test_to_date_future(dialysis):
    dialysis.to_date = date.today() + timedelta(days=1)
    invalid(dialysis)


def test_to_date_before_from_date(dialysis):
    dialysis.to_date = dialysis.from_date - timedelta(days=1)
    invalid(dialysis)


def test_type_of_dialysis_missing(dialysis):
    dialysis.type_of_dialysis = None
    invalid(dialysis)


def test_type_of_dialysis_invalid(dialysis):
    dialysis.type_of_dialysis = 0
    invalid(dialysis)


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(Dialysis, DialysisValidation, obj, **kwargs)
