from datetime import date

import pytest

from radar.lib.models import SaltWastingClinicalFeatures, PatientDemographics, Patient
from radar.lib.validation.core import ValidationError
from radar.lib.validation.salt_wasting import SaltWastingClinicalFeaturesValidation
from utils import validation_runner


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


def valid(obj, **kwargs):
    return validate(obj, **kwargs)


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        validate(obj, **kwargs)

    return e


def validate(obj, **kwargs):
    return validation_runner(SaltWastingClinicalFeatures, SaltWastingClinicalFeaturesValidation, obj, **kwargs)
