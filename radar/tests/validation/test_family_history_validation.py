import pytest

from radar.models import Patient, Cohort
from radar.models.family_history import FamilyHistory
from radar.validation.core import ValidationError
from radar.validation.family_history import FamilyHistoryValidation
from helpers.validation import validation_runner


@pytest.fixture
def family_history():
    obj = FamilyHistory()
    obj.patient = Patient()
    obj.cohort = Cohort()
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


def test_cohort_missing(family_history):
    family_history.cohort = None
    invalid(family_history)


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
