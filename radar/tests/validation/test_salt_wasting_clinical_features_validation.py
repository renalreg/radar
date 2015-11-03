from datetime import date

import pytest

from radar.models import SaltWastingClinicalFeatures, PatientDemographics, Patient
from radar.validation.core import ValidationError
from radar.validation.salt_wasting import SaltWastingClinicalFeaturesValidation
from helpers.validation import validation_runner


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def clinical_features(patient):
    obj = SaltWastingClinicalFeatures()
    obj.patient = patient
    obj.normal_pregnancy = False
    obj.abnormal_pregnancy_text = 'Foo'
    obj.neurological_problems = True
    obj.seizures = True
    obj.abnormal_gait = True
    obj.deafness = True
    obj.other_neurological_problem = True
    obj.other_neurological_problem_text = 'Bar'
    obj.joint_problems = True
    obj.joint_problems_age = 21
    obj.x_ray_abnormalities = True
    obj.chondrocalcinosis = True
    obj.other_x_ray_abnormality = True
    obj.other_x_ray_abnormality_text = 'Baz'
    return obj


def test_valid(clinical_features):
    obj = valid(clinical_features)
    assert obj.normal_pregnancy is False
    assert obj.abnormal_pregnancy_text == 'Foo'
    assert obj.neurological_problems is True
    assert obj.seizures is True
    assert obj.abnormal_gait is True
    assert obj.deafness is True
    assert obj.other_neurological_problem is True
    assert obj.other_neurological_problem_text == 'Bar'
    assert obj.joint_problems is True
    assert obj.joint_problems_age == 21
    assert obj.x_ray_abnormalities is True
    assert obj.chondrocalcinosis is True
    assert obj.other_x_ray_abnormality is True
    assert obj.other_x_ray_abnormality_text == 'Baz'


def test_normal_pregnancy_true(clinical_features):
    clinical_features.normal_pregnancy = True
    obj = valid(clinical_features)
    assert obj.abnormal_pregnancy_text is None


def test_normal_pregnancy_true_missing(clinical_features):
    clinical_features.normal_pregnancy = None
    invalid(clinical_features)


def test_normal_pregnancy_true_text_missing(clinical_features):
    clinical_features.normal_pregnancy = True
    clinical_features.abnormal_pregnancy_text = None
    obj = valid(clinical_features)
    assert obj.abnormal_pregnancy_text is None


def test_normal_pregnancy_true_text_blank(clinical_features):
    clinical_features.normal_pregnancy = True
    clinical_features.abnormal_pregnancy_text = ''
    obj = valid(clinical_features)
    assert obj.abnormal_pregnancy_text is None


def test_normal_pregnancy_false_text_missing(clinical_features):
    clinical_features.abnormal_pregnancy_text = None
    invalid(clinical_features)


def test_normal_pregnancy_false_text_blank(clinical_features):
    clinical_features.abnormal_pregnancy_text = ''
    invalid(clinical_features)


def test_neurological_problems_false(clinical_features):
    obj = valid(clinical_features)
    obj.seizures = None
    obj.abnormal_gait = None
    obj.deafness = None
    obj.other_neurological_problem = None
    obj.other_neurological_problem_text = None


def test_neurological_problems_missing(clinical_features):
    clinical_features.neurological_problems = None
    invalid(clinical_features)


def test_neurological_problems_true_seizures_missing(clinical_features):
    clinical_features.seizures = None
    invalid(clinical_features)


def test_neurological_problems_false_seizures_missing(clinical_features):
    clinical_features.neurological_problems = False
    clinical_features.seizures = None
    valid(clinical_features)


def test_neurological_problems_true_abnormal_gait_missing(clinical_features):
    clinical_features.abnormal_gait = None
    invalid(clinical_features)


def test_neurological_problems_false_abnormal_gait_missing(clinical_features):
    clinical_features.neurological_problems = False
    clinical_features.abnormal_gait = None
    valid(clinical_features)


def test_neurological_problems_true_deafness_missing(clinical_features):
    clinical_features.deafness = None
    invalid(clinical_features)


def test_neurological_problems_false_deafness_missing(clinical_features):
    clinical_features.neurological_problems = False
    clinical_features.deafness = None
    valid(clinical_features)


def test_neurological_problems_true_other_neurological_problem_missing(clinical_features):
    clinical_features.other_neurological_problem = None
    invalid(clinical_features)


def test_other_neurological_problem_false_text_missing(clinical_features):
    clinical_features.other_neurological_problem = False
    clinical_features.other_neurological_problem_text = None
    valid(clinical_features)


def test_other_neurological_problem_true_text_blank(clinical_features):
    clinical_features.other_neurological_problem_text = ''
    invalid(clinical_features)


def test_other_neurological_problem_true_text_missing(clinical_features):
    clinical_features.other_neurological_problem_text = None
    invalid(clinical_features)


def test_joint_problems_false(clinical_features):
    clinical_features.joint_problems = False
    obj = valid(clinical_features)
    assert obj.joint_problems_age is None
    assert obj.x_ray_abnormalities is None
    assert obj.chondrocalcinosis is None
    assert obj.other_x_ray_abnormality is None
    assert obj.other_x_ray_abnormality_text is None


def test_joint_problems_missing(clinical_features):
    clinical_features.neurological_problems = None
    invalid(clinical_features)


def test_joint_problems_true_joint_problems_age_missing(clinical_features):
    clinical_features.joint_problems_age = None
    invalid(clinical_features)


def test_joint_problems_false_joint_problems_age_missing(clinical_features):
    clinical_features.joint_problems = False
    clinical_features.joint_problems_age = None
    valid(clinical_features)


def test_joint_problems_true_joint_problems_age_too_young(clinical_features):
    clinical_features.joint_problems_age = -1
    invalid(clinical_features)


def test_joint_problems_true_joint_problems_age_too_old(clinical_features):
    clinical_features.joint_problems_age = 121
    invalid(clinical_features)


def test_joint_problems_true_x_ray_abnormalities_missing(clinical_features):
    clinical_features.x_ray_abnormalities = None
    invalid(clinical_features)


def test_joint_problems_false_x_ray_abnormalities_missing(clinical_features):
    clinical_features.joint_problems = False
    clinical_features.x_ray_abnormalities = None
    valid(clinical_features)


def test_joint_problems_true_chondrocalcinosis_missing(clinical_features):
    clinical_features.chondrocalcinosis = None
    invalid(clinical_features)


def test_joint_problems_false_chondrocalcinosis_missing(clinical_features):
    clinical_features.joint_problems = False
    clinical_features.chondrocalcinosis = None
    valid(clinical_features)


def test_joint_problems_true_other_x_ray_abnormality_missing(clinical_features):
    clinical_features.other_x_ray_abnormality = None
    invalid(clinical_features)


def test_joint_problems_false_other_x_ray_abnormality_missing(clinical_features):
    clinical_features.joint_problems = False
    clinical_features.other_x_ray_abnormality = None
    valid(clinical_features)


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(SaltWastingClinicalFeatures, SaltWastingClinicalFeaturesValidation, obj, **kwargs)
