import pytest

from radar.models.patients import Patient
from radar.models.groups import Group, GROUP_TYPE, GroupPatient
from radar.models.family_histories import FamilyHistory
from radar.validation.core import ValidationError
from radar.validation.family_histories import FamilyHistoryValidation
from radar.tests.validation.helpers import validation_runner
from radar.exceptions import PermissionDenied


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
    obj = FamilyHistory()
    obj.patient = patient
    obj.group = group
    obj.parental_consanguinity = True
    obj.family_history = True
    obj.other_family_history = 'Hello World!'
    return obj


def test_valid(family_history):
    obj = valid(family_history)
    assert obj.parental_consanguinity is True
    assert obj.family_history is True
    assert obj.other_family_history == 'Hello World!'


def test_patient_missing(family_history):
    family_history.patient = None
    invalid(family_history)


def test_group_missing(family_history):
    family_history.group = None
    invalid(family_history)


def test_group_not_cohort(family_history):
    family_history.group.type = GROUP_TYPE.OTHER

    with pytest.raises(PermissionDenied):
        valid(family_history)


def test_parental_consanguinity_missing(family_history):
    family_history.parental_consanguinity = None
    invalid(family_history)


def test_parental_consanguinity_true(family_history):
    family_history.parental_consanguinity = True
    obj = valid(family_history)
    assert obj.parental_consanguinity is True


def test_parental_consanguinity_false(family_history):
    family_history.parental_consanguinity = False
    obj = valid(family_history)
    assert obj.parental_consanguinity is False


def test_family_history_missing(family_history):
    family_history.family_history = None
    invalid(family_history)


def test_family_history_true(family_history):
    family_history.family_history = True
    obj = valid(family_history)
    assert obj.family_history is True


def test_family_history_false(family_history):
    family_history.family_history = False
    obj = valid(family_history)
    assert obj.family_history is False


def test_other_family_history_missing(family_history):
    family_history.other_family_history = None
    obj = valid(family_history)
    obj.other_family_history = None


def test_other_family_history_blank(family_history):
    family_history.other_family_history = ''
    obj = valid(family_history)
    obj.other_family_history = None


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(FamilyHistory, FamilyHistoryValidation, obj, **kwargs)
