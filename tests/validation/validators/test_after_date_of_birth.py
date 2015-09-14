from datetime import datetime, date
import pytest
import pytz
from radar.lib.models import Patient, PatientDemographics
from radar.lib.validation.core import ValidationError, ValidatorCall
from radar.lib.validation.validators import after_date_of_birth


def call_after_date_of_birth(date_of_birth, value):
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date_of_birth
    patient.patient_demographics.append(patient_demographics)

    ctx = {'patient': patient}
    call = ValidatorCall(ctx, None)

    return call(after_date_of_birth(), value)


def test_no_date_of_birth():
    call_after_date_of_birth(None, date(1999, 1, 1))


def test_less_than():
    with pytest.raises(ValidationError):
        call_after_date_of_birth(date(2000, 1, 1), date(1999, 12, 31))


def test_equal():
    call_after_date_of_birth(date(2000, 1, 1), date(2000, 1, 1))


def test_greater_than():
    call_after_date_of_birth(date(2000, 1, 1), date(2000, 1, 2))


def test_datetime():
    call_after_date_of_birth(date(2000, 1, 1), datetime(2000, 1, 2, tzinfo=pytz.utc))
