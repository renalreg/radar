from datetime import date, timedelta

import pytest

from radar.models import Patient, PatientDemographics, Diagnosis, Cohort, \
    CohortDiagnosis
from radar.validation.core import ValidationError
from radar.validation.diagnoses import DiagnosisValidation
from radar.tests.validation.helpers import validation_runner


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def diagnosis(patient):
    cohort = Cohort(id=1)

    obj = Diagnosis()
    obj.patient = patient
    obj.cohort = cohort
    obj.date = date(2015, 1, 1)
    obj.cohort_diagnosis = CohortDiagnosis(cohort=cohort)
    obj.diagnosis_text = 'Foo Bar Baz'
    obj.biopsy_diagnosis = 1

    return obj


def test_valid(diagnosis):
    obj = valid(diagnosis)
    assert obj.patient is not None
    assert obj.cohort is not None
    assert obj.date == date(2015, 1, 1)
    assert obj.cohort_diagnosis is not None
    assert obj.diagnosis_text == 'Foo Bar Baz'
    assert obj.biopsy_diagnosis == 1
    assert obj.created_user is not None
    assert obj.created_date is not None
    assert obj.modified_user is not None
    assert obj.modified_date is not None


def test_patient_missing(diagnosis):
    diagnosis.patient = None
    invalid(diagnosis)


def test_cohort_missing(diagnosis):
    diagnosis.cohort = None
    invalid(diagnosis)


def test_date_missing(diagnosis):
    diagnosis.date = None
    invalid(diagnosis)


def test_date_before_dob(diagnosis):
    diagnosis.date = date(1999, 1, 1)
    invalid(diagnosis)


def test_date_in_future(diagnosis):
    diagnosis.date = date.today() + timedelta(days=1)
    invalid(diagnosis)


def test_cohort_diagnosis_missing(diagnosis):
    diagnosis.cohort_diagnosis = None
    invalid(diagnosis)


def test_cohort_diagnosis_from_another_cohort(diagnosis):
    diagnosis.cohort_diagnosis = CohortDiagnosis(cohort=Cohort(id=2))
    invalid(diagnosis)


def test_diagnosis_text_missing(diagnosis):
    diagnosis.diagnosis_text = None
    obj = valid(diagnosis)
    assert obj.diagnosis_text is None


def test_diagnosis_text_blank(diagnosis):
    diagnosis.diagnosis_text = ''
    obj = valid(diagnosis)
    assert obj.diagnosis_text is None


def test_biopsy_diagnosis_missing(diagnosis):
    diagnosis.biopsy_diagnosis = None
    obj = valid(diagnosis)
    assert obj.biopsy_diagnosis is None


def test_biopsy_diagnosis_invalid(diagnosis):
    diagnosis.biopsy_diagnosis = 99999
    invalid(diagnosis)


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(Diagnosis, DiagnosisValidation, obj, **kwargs)
