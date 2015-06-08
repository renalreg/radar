from datetime import date, timedelta

import pytest

from radar.lib.validation.core import ErrorHandler
from radar.lib.validation.transplants import validate_transplant
from radar.models import Patient, PatientDemographics, Plasmapheresis, PlasmapheresisResponse, Transplant, \
    TransplantType


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.demographics_list.append(patient_demographics)
    return patient


@pytest.fixture
def transplant(patient):
    transplant = Transplant()
    transplant.patient = patient
    transplant.transplant_date = date(2015, 1, 1)
    transplant.transplant_type = TransplantType(id=1)
    return transplant


@pytest.fixture
def errors():
    errors = ErrorHandler()
    return errors


def test_transplant_valid(errors, transplant):
    validate_transplant(errors, transplant)
    assert errors.is_valid()


def test_transplant_transplant_date_missing(errors, transplant):
    transplant.transplant_date = None
    validate_transplant(errors, transplant)
    assert not errors.is_valid()


def test_transplant_transplant_date_before_dob(errors, transplant):
    transplant.transplant_date = date(1999, 1, 1)
    validate_transplant(errors, transplant)
    assert not errors.is_valid()


def test_transplant_transplant_date_future(errors, transplant):
    transplant.transplant_date = date.today() + timedelta(days=1)
    validate_transplant(errors, transplant)
    assert not errors.is_valid()


def test_transplant_transplant_type_missing(errors, transplant):
    transplant.transplant_type = None
    validate_transplant(errors, transplant)
    assert not errors.is_valid()
