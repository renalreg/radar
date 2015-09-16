import pytest
from radar.lib.models import Patient, CohortPatient, Cohort
from radar.lib.validation.cohort_patients import CohortPatientValidation
from radar.lib.validation.core import ValidationError
from utils import validation_runner


@pytest.fixture
def cohort_patient():
    obj = CohortPatient()
    obj.patient = Patient()
    obj.cohort = Cohort()
    return obj


def test_valid(cohort_patient):
    obj = valid(cohort_patient)
    assert obj.patient is not None
    assert obj.cohort is not None


def test_patient_missing(cohort_patient):
    cohort_patient.patient = None
    invalid(cohort_patient)


def test_cohort_missing(cohort_patient):
    cohort_patient.cohort = None
    invalid(cohort_patient)


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(CohortPatient, CohortPatientValidation, obj, **kwargs)
