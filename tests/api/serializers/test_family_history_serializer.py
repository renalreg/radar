from cornflake.exceptions import ValidationError
import pytest

from radar.api.serializers.family_histories import FamilyHistorySerializer
from radar.exceptions import PermissionDenied
from radar.models.groups import Group, GROUP_TYPE, GroupPatient
from radar.models.patients import Patient
from radar.models.users import User


@pytest.fixture
def group():
    return Group(type=GROUP_TYPE.COHORT)


@pytest.fixture
def patient(group):
    patient = Patient()

    group_patient = GroupPatient()
    group_patient.group = group
    group_patient.patient = patient

    return patient


@pytest.fixture
def family_history(patient, group):
    return {
        'patient': patient,
        'group': group,
        'parental_consanguinity': True,
        'family_history': True,
        'other_family_history': 'Hello World!'
    }


def test_valid(family_history):
    obj = valid(family_history)
    assert obj.parental_consanguinity is True
    assert obj.family_history is True
    assert obj.other_family_history == 'Hello World!'


def test_patient_none(family_history):
    family_history['patient'] = None
    invalid(family_history)


def test_group_none(family_history):
    family_history['group'] = None
    invalid(family_history)


def test_group_not_cohort(family_history):
    family_history['group'].type = GROUP_TYPE.OTHER

    with pytest.raises(PermissionDenied):
        valid(family_history)


def test_parental_consanguinity_none(family_history):
    family_history['parental_consanguinity'] = None
    invalid(family_history)


def test_parental_consanguinity_true(family_history):
    family_history['parental_consanguinity'] = True
    obj = valid(family_history)
    assert obj.parental_consanguinity is True


def test_parental_consanguinity_false(family_history):
    family_history['parental_consanguinity'] = False
    obj = valid(family_history)
    assert obj.parental_consanguinity is False


def test_family_history_none(family_history):
    family_history['family_history'] = None
    invalid(family_history)


def test_family_history_true(family_history):
    family_history['family_history'] = True
    obj = valid(family_history)
    assert obj.family_history is True


def test_family_history_false(family_history):
    family_history['family_history'] = False
    obj = valid(family_history)
    assert obj.family_history is False


def test_other_family_history_none(family_history):
    family_history['other_family_history'] = None
    obj = valid(family_history)
    obj.other_family_history = None


def test_other_family_history_blank(family_history):
    family_history['other_family_history'] = ''
    obj = valid(family_history)
    obj.other_family_history = None


def invalid(data):
    with pytest.raises(ValidationError) as e:
        valid(data)

    return e


def valid(data):
    serializer = FamilyHistorySerializer(data=data, context={'user': User(is_admin=True)})
    serializer.is_valid(raise_exception=True)
    return serializer.save()
