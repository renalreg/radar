from datetime import date, timedelta

import pytest

from radar.lib.models import Dialysis, DialysisType, Patient, PatientDemographics, User, DataSource
from radar.lib.validation.core import ValidationError
from radar.lib.validation.dialysis import DialysisValidation


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def dialysis(patient):
    dialysis = Dialysis()
    dialysis.data_source = DataSource()
    dialysis.patient = patient
    dialysis.from_date = date(2015, 1, 1)
    dialysis.to_date = date(2015, 1, 2)
    dialysis.dialysis_type = DialysisType(id=1)
    return dialysis


def test_dialysis_valid(dialysis):
    valid(dialysis)


def test_dialysis_from_date_missing(dialysis):
    dialysis.from_date = None
    invalid(dialysis)


def test_dialysis_from_date_before_dob(dialysis):
    dialysis.from_date = date(1999, 1, 1)
    invalid(dialysis)


def test_dialysis_from_date_future(dialysis):
    dialysis.from_date = date.today() + timedelta(days=1)
    invalid(dialysis)


def test_dialysis_to_date_missing(dialysis):
    dialysis.to_date = None
    valid(dialysis)


def test_dialysis_to_date_before_dob(dialysis):
    dialysis.to_date = date(1999, 1, 1)
    invalid(dialysis)


def test_dialysis_to_date_future(dialysis):
    dialysis.to_date = date.today() + timedelta(days=1)
    invalid(dialysis)


def test_dialysis_to_date_before_from_date(dialysis):
    dialysis.to_date = dialysis.from_date - timedelta(days=1)
    invalid(dialysis)


def test_dialysis_dialysis_type_missing(dialysis):
    dialysis.dialysis_type = None
    invalid(dialysis)


def valid(dialysis):
    validate(dialysis)


def invalid(dialysis):
    with pytest.raises(ValidationError):
        validate(dialysis)


def validate(dialysis):
    validation = DialysisValidation()
    ctx = {'user': User(is_admin=True)}
    validation.before_update(ctx, Dialysis())
    old_obj = validation.clone(dialysis)
    validation.after_update(ctx, old_obj, dialysis)
