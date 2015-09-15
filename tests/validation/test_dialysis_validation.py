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
    obj = Dialysis()
    obj.data_source = DataSource()
    obj.patient = patient
    obj.from_date = date(2015, 1, 1)
    obj.to_date = date(2015, 1, 2)
    obj.dialysis_type = DialysisType(id=1)
    return obj


def test_valid(dialysis):
    obj = valid(dialysis)
    assert obj.from_date == date(2015, 1, 1)
    assert obj.to_date == date(2015, 1, 2)
    assert obj.dialysis_type.id == 1
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


def test_dialysis_type_missing(dialysis):
    dialysis.dialysis_type = None
    invalid(dialysis)


def valid(dialysis):
    return validate(dialysis)


def invalid(dialysis):
    with pytest.raises(ValidationError) as e:
        validate(dialysis)

    return e


def validate(dialysis):
    validation = DialysisValidation()
    ctx = {'user': User(is_admin=True)}
    validation.before_update(ctx, Dialysis())
    old_obj = validation.clone(dialysis)
    obj = validation.after_update(ctx, old_obj, dialysis)
    return obj
