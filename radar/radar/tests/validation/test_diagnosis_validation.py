from datetime import date, timedelta

import pytest

from radar.models.patients import Patient
from radar.models.patient_demographics import PatientDemographics
from radar.models.diagnoses import Diagnosis, GroupDiagnosis
from radar.models.groups import Group, GROUP_TYPE_COHORT, GROUP_TYPE_OTHER
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
    group = Group(type=GROUP_TYPE_COHORT)

    obj = Diagnosis()
    obj.patient = patient
    obj.group = group
    obj.date_of_symptoms = date(2014, 1, 1)
    obj.date_of_diagnosis = date(2015, 1, 1)
    obj.group_diganosis = GroupDiagnosis(group=group)
    obj.diagnosis_text = 'Foo Bar Baz'
    obj.biopsy_diagnosis = 1

    return obj


def test_valid(diagnosis):
    obj = valid(diagnosis)
    assert obj.patient is not None
    assert obj.group is not None
    assert obj.date_of_symptoms == date(2014, 1, 1)
    assert obj.date_of_diagnosis == date(2015, 1, 1)
    assert obj.group_diganosis is not None
    assert obj.diagnosis_text == 'Foo Bar Baz'
    assert obj.biopsy_diagnosis == 1
    assert obj.created_user is not None
    assert obj.created_date is not None
    assert obj.modified_user is not None
    assert obj.modified_date is not None


def test_patient_missing(diagnosis):
    diagnosis.patient = None
    invalid(diagnosis)


def test_group_missing(diagnosis):
    diagnosis.group = None
    invalid(diagnosis)


def test_group_not_cohort(diagnosis):
    diagnosis.group.type == GROUP_TYPE_OTHER
    invalid(diagnosis)


def test_date_of_symptoms_missing(diagnosis):
    diagnosis.date_of_symptoms = None
    invalid(diagnosis)


def test_date_of_symptoms_before_dob(diagnosis):
    diagnosis.date_of_symptoms = date(1999, 1, 1)
    invalid(diagnosis)


def test_date_of_symptoms_in_future(diagnosis):
    diagnosis.date_of_symptoms = date.today() + timedelta(days=1)
    invalid(diagnosis)


def test_date_of_diagnosis_missing(diagnosis):
    diagnosis.date_of_diagnosis = None
    invalid(diagnosis)


def test_date_of_diagnosis_before_dob(diagnosis):
    diagnosis.date_of_diagnosis = date(1999, 1, 1)
    invalid(diagnosis)


def test_date_of_diagnosis_in_future(diagnosis):
    diagnosis.date_of_diagnosis = date.today() + timedelta(days=1)
    invalid(diagnosis)


def test_date_of_diagnosis_before_date_of_symptoms(diagnosis):
    diagnosis.date_of_diagnosis = diagnosis.date_of_symptoms - timedelta(days=1)
    invalid(diagnosis)


def test_group_diagnosis_missing(diagnosis):
    diagnosis.group_diagnosis = None
    invalid(diagnosis)


def test_group_diagnosis_from_another_cohort(diagnosis):
    diagnosis.group_diagnosis = GroupDiagnosis(group=Group(type=GROUP_TYPE_COHORT))
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
