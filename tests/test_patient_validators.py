from datetime import date
import pytest
from radar.lib.validation.core import ValidationError
from radar.lib.validation.patient_validators import after_date_of_birth
from radar.models import Patient, PatientDemographics


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.demographics_list.append(patient_demographics)
    return patient


def test_after_date_of_birth_no_date_of_birth():
    patient = Patient()
    after_date_of_birth(patient)(date(1999, 1, 1))


def test_after_date_of_birth_less_than(patient):
    with pytest.raises(ValidationError):
        after_date_of_birth(patient)(date(1999, 12, 31))


def test_after_date_of_birth_equal(patient):
    after_date_of_birth(patient)(date(2000, 1, 1))


def test_after_date_of_birth_greater_than(patient):
    after_date_of_birth(patient)(date(2000, 1, 2))
