from datetime import date, timedelta

import pytest

from radar.lib.models import Patient, PatientDemographics, Transplant, DataSource, User
from radar.lib.validation.core import ValidationError
from radar.lib.validation.transplants import TransplantValidation


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def transplant(patient):
    transplant = Transplant()
    transplant.data_source = DataSource()
    transplant.patient = patient
    transplant.transplant_date = date(2015, 1, 1)
    transplant.transplant_type = 'FOO'  # TODO
    return transplant


def test_valid(transplant):
    valid(transplant)


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


def valid(transplant):
    validate(transplant)


def invalid(transplant):
    with pytest.raises(ValidationError):
        validate(transplant)


def validate(transplant):
    validation = TransplantValidation()
    ctx = {'user': User(is_admin=True)}
    validation.before_update(ctx, Transplant())
    old_obj = validation.clone(transplant)
    validation.after_update(ctx, old_obj, transplant)
