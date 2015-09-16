import pytest

from radar.lib.models import Patient
from radar.lib.models.family_history import FamilyHistory
from radar.lib.validation.core import ValidationError
from radar.lib.validation.family_history import FamilyHistoryValidation
from utils import validation_runner


@pytest.fixture
def family_history():
    obj = FamilyHistory()
    obj.patient = Patient()
    obj.parental_consanguinity = True
    obj.family_history = True
    return obj


def test_valid(family_history):
    obj = valid(family_history)
    assert obj.parental_consanguinity is True
    assert obj.family_history is True


def test_patient_missing(family_history):
    family_history.patient = None
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


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(FamilyHistory, FamilyHistoryValidation, obj, **kwargs)
