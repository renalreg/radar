from datetime import date

import pytest
from cornflake.exceptions import ValidationError

from radar.api.serializers.salt_wasting import SaltWastingClinicalFeaturesSerializer
from radar.models.patient_demographics import PatientDemographics
from radar.models.patients import Patient
from radar.models.users import User


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def clinical_features(patient):
    return {
        'patient': patient,
        'normal_pregnancy': False,
        'abnormal_pregnancy_text': 'Foo',
        'neurological_problems': True,
        'seizures': True,
        'abnormal_gait': True,
        'deafness': True,
        'other_neurological_problem': True,
        'other_neurological_problem_text': 'Bar',
        'joint_problems': True,
        'joint_problems_age': 21,
        'x_ray_abnormalities': True,
        'chondrocalcinosis': True,
        'other_x_ray_abnormality': True,
        'other_x_ray_abnormality_text': 'Baz'
    }


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
    clinical_features['normal_pregnancy'] = True
    obj = valid(clinical_features)
    assert obj.abnormal_pregnancy_text is None


def test_normal_pregnancy_true_none(clinical_features):
    clinical_features['normal_pregnancy'] = None
    valid(clinical_features)


def test_normal_pregnancy_true_text_none(clinical_features):
    clinical_features['normal_pregnancy'] = True
    clinical_features['abnormal_pregnancy_text'] = None
    obj = valid(clinical_features)
    assert obj.abnormal_pregnancy_text is None


def test_normal_pregnancy_true_text_blank(clinical_features):
    clinical_features['normal_pregnancy'] = True
    clinical_features['abnormal_pregnancy_text'] = ''
    obj = valid(clinical_features)
    assert obj.abnormal_pregnancy_text is None


def test_normal_pregnancy_false_text_none(clinical_features):
    clinical_features['abnormal_pregnancy_text'] = None
    invalid(clinical_features)


def test_normal_pregnancy_false_text_blank(clinical_features):
    clinical_features['abnormal_pregnancy_text'] = ''
    invalid(clinical_features)


def test_neurological_problems_false(clinical_features):
    obj = valid(clinical_features)
    obj.seizures = None
    obj.abnormal_gait = None
    obj.deafness = None
    obj.other_neurological_problem = None
    obj.other_neurological_problem_text = None


def test_neurological_problems_none(clinical_features):
    clinical_features['neurological_problems'] = None
    valid(clinical_features)


def test_neurological_problems_true_seizures_none(clinical_features):
    clinical_features['seizures'] = None
    invalid(clinical_features)


def test_neurological_problems_false_seizures_none(clinical_features):
    clinical_features['neurological_problems'] = False
    clinical_features['seizures'] = None
    valid(clinical_features)


def test_neurological_problems_true_abnormal_gait_none(clinical_features):
    clinical_features['abnormal_gait'] = None
    invalid(clinical_features)


def test_neurological_problems_false_abnormal_gait_none(clinical_features):
    clinical_features['neurological_problems'] = False
    clinical_features['abnormal_gait'] = None
    valid(clinical_features)


def test_neurological_problems_true_deafness_none(clinical_features):
    clinical_features['deafness'] = None
    invalid(clinical_features)


def test_neurological_problems_false_deafness_none(clinical_features):
    clinical_features['neurological_problems'] = False
    clinical_features['deafness'] = None
    valid(clinical_features)


def test_neurological_problems_true_other_neurological_problem_none(clinical_features):
    clinical_features['other_neurological_problem'] = None
    invalid(clinical_features)


def test_other_neurological_problem_false_text_none(clinical_features):
    clinical_features['other_neurological_problem'] = False
    clinical_features['other_neurological_problem_text'] = None
    valid(clinical_features)


def test_other_neurological_problem_true_text_blank(clinical_features):
    clinical_features['other_neurological_problem_text'] = ''
    invalid(clinical_features)


def test_other_neurological_problem_true_text_none(clinical_features):
    clinical_features['other_neurological_problem_text'] = None
    invalid(clinical_features)


def test_joint_problems_false(clinical_features):
    clinical_features['joint_problems'] = False
    obj = valid(clinical_features)
    assert obj.joint_problems_age is None
    assert obj.x_ray_abnormalities is None
    assert obj.chondrocalcinosis is None
    assert obj.other_x_ray_abnormality is None
    assert obj.other_x_ray_abnormality_text is None


def test_joint_problems_none(clinical_features):
    clinical_features['neurological_problems'] = None
    valid(clinical_features)


def test_joint_problems_true_joint_problems_age_none(clinical_features):
    clinical_features['joint_problems_age'] = None
    invalid(clinical_features)


def test_joint_problems_false_joint_problems_age_none(clinical_features):
    clinical_features['joint_problems'] = False
    clinical_features['joint_problems_age'] = None
    valid(clinical_features)


def test_joint_problems_true_joint_problems_age_too_young(clinical_features):
    clinical_features['joint_problems_age'] = -1
    invalid(clinical_features)


def test_joint_problems_true_joint_problems_age_too_old(clinical_features):
    clinical_features['x_ray_abnormalities'] = 121
    invalid(clinical_features)


def test_joint_problems_true_x_ray_abnormalities_none(clinical_features):
    clinical_features['x_ray_abnormalities'] = None
    invalid(clinical_features)


def test_joint_problems_false_x_ray_abnormalities_none(clinical_features):
    clinical_features['joint_problems'] = False
    clinical_features['x_ray_abnormalities'] = None
    valid(clinical_features)


def test_joint_problems_true_chondrocalcinosis_none(clinical_features):
    clinical_features['chondrocalcinosis'] = None
    invalid(clinical_features)


def test_joint_problems_false_chondrocalcinosis_none(clinical_features):
    clinical_features['joint_problems'] = False
    clinical_features['chondrocalcinosis'] = None
    valid(clinical_features)


def test_joint_problems_true_other_x_ray_abnormality_none(clinical_features):
    clinical_features['other_x_ray_abnormality'] = None
    invalid(clinical_features)


def test_joint_problems_false_other_x_ray_abnormality_none(clinical_features):
    clinical_features['joint_problems'] = False
    clinical_features['other_x_ray_abnormality'] = None
    valid(clinical_features)


def invalid(data):
    with pytest.raises(ValidationError) as e:
        valid(data)

    return e


def valid(data):
    serializer = SaltWastingClinicalFeaturesSerializer(data=data, context={'user': User(is_admin=True)})
    serializer.is_valid(raise_exception=True)
    return serializer.save()
