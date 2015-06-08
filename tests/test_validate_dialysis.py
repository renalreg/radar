from datetime import date, timedelta
import pytest
from radar.lib.validation.core import ErrorHandler
from radar.lib.validation.dialysis import validate_dialysis
from radar.models import Dialysis, DialysisType, Patient, PatientDemographics


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.demographics_list.append(patient_demographics)
    return patient


@pytest.fixture
def dialysis(patient):
    dialysis = Dialysis()
    dialysis.patient = patient
    dialysis.from_date = date(2015, 1, 1)
    dialysis.to_date = date(2015, 1, 2)
    dialysis.dialysis_type = DialysisType(id=1)
    return dialysis


@pytest.fixture
def errors():
    errors = ErrorHandler()
    return errors


def test_dialysis_valid(errors, dialysis):
    validate_dialysis(errors, dialysis)
    assert errors.is_valid()


def test_dialysis_from_date_missing(errors, dialysis):
    dialysis.from_date = None
    validate_dialysis(errors, dialysis)
    assert not errors.is_valid()


def test_dialysis_from_date_before_dob(errors, dialysis):
    dialysis.from_date = date(1999, 1, 1)
    validate_dialysis(errors, dialysis)
    assert not errors.is_valid()


def test_dialysis_from_date_future(errors, dialysis):
    dialysis.from_date = date.today() + timedelta(days=1)
    validate_dialysis(errors, dialysis)
    assert not errors.is_valid()


def test_dialysis_to_date_missing(errors, dialysis):
    dialysis.to_date = None
    validate_dialysis(errors, dialysis)
    assert errors.is_valid()


def test_dialysis_to_date_before_dob(errors, dialysis):
    dialysis.to_date = date(1999, 1, 1)
    validate_dialysis(errors, dialysis)
    assert not errors.is_valid()


def test_dialysis_to_date_future(errors, dialysis):
    dialysis.to_date = date.today() + timedelta(days=1)
    validate_dialysis(errors, dialysis)
    assert not errors.is_valid()


def test_dialysis_to_date_before_from_date(errors, dialysis):
    dialysis.to_date = dialysis.from_date - timedelta(days=1)
    validate_dialysis(errors, dialysis)
    assert not errors.is_valid()


def test_dialysis_dialysis_type_missing(errors, dialysis):
    dialysis.dialysis_type = None
    validate_dialysis(errors, dialysis)
    assert not errors.is_valid()
