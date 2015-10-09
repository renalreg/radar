from datetime import date, timedelta
import pytest
from radar.lib.models import Patient, PatientDemographics
from radar.lib.validation.core import ValidatorCall, ValidationError
from radar.lib.validation.validators import valid_date_for_patient


def test_before_dob():
    with pytest.raises(ValidationError):
        call_valid_date_for_patient(date(2000, 1, 1), date(1999, 12, 31))


def test_on_dob():
    value = call_valid_date_for_patient(date(2000, 1, 1), date(2000, 1, 1))
    assert value == date(2000, 1, 1)


def test_after_dob():
    value = call_valid_date_for_patient(date(2000, 1, 1), date(2000, 1, 2))
    assert value == date(2000, 1, 2)


def test_in_future():
    with pytest.raises(ValidationError):
        call_valid_date_for_patient(date(2000, 1, 1), date.today() + timedelta(days=1))


def test_before_day_zero():
    with pytest.raises(ValidationError):
        call_valid_date_for_patient(date(1800, 1, 1), date(1899, 12, 31))


def call_valid_date_for_patient(date_of_birth, value):
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date_of_birth
    patient.patient_demographics.append(patient_demographics)

    ctx = {'patient': patient}
    call = ValidatorCall(ctx, None)

    return call(valid_date_for_patient(), value)
