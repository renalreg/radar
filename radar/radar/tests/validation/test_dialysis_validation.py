from datetime import date, timedelta

import pytest

from radar.models import Dialysis, Patient, PatientDemographics
from radar.models.groups import Group
from radar.models.source_types import SOURCE_TYPE_RADAR
from radar.validation.core import ValidationError
from radar.validation.dialysis import DialysisValidation
from radar.tests.validation.helpers import validation_runner


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def dialysis(patient):
    obj = Dialysis()
    obj.source_group = Group()
    obj.source_type = SOURCE_TYPE_RADAR
    obj.patient = patient
    obj.from_date = date(2015, 1, 1)
    obj.to_date = date(2015, 1, 2)
    obj.modality = 1
    return obj


def test_valid(dialysis):
    obj = valid(dialysis)
    assert obj.from_date == date(2015, 1, 1)
    assert obj.to_date == date(2015, 1, 2)
    assert obj.modality == 1
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_missing(dialysis):
    dialysis.patient = None
    invalid(dialysis)


def test_source_group_missing(dialysis):
    dialysis.source_group = None
    invalid(dialysis)


def test_source_type_missing(dialysis):
    dialysis.source_type = None
    dialysis = valid(dialysis)
    assert dialysis.source_type == 'RADAR'


def test_from_date_missing(dialysis):
    dialysis.from_date = None
    invalid(dialysis)


def test_from_date_before_dob(dialysis):
    dialysis.from_date = date(1999, 1, 1)
    invalid(dialysis)


def test_from_date_future(dialysis):
    dialysis.from_date = date.today() + timedelta(days=1)
    invalid(dialysis)


def test_to_date_missing(dialysis):
    dialysis.to_date = None
    valid(dialysis)


def test_to_date_before_dob(dialysis):
    dialysis.to_date = date(1999, 1, 1)
    invalid(dialysis)


def test_to_date_future(dialysis):
    dialysis.to_date = date.today() + timedelta(days=1)
    invalid(dialysis)


def test_to_date_before_from_date(dialysis):
    dialysis.to_date = dialysis.from_date - timedelta(days=1)
    invalid(dialysis)


def test_modality_missing(dialysis):
    dialysis.modality = None
    invalid(dialysis)


def test_modality_invalid(dialysis):
    dialysis.modality = 0
    invalid(dialysis)


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(Dialysis, DialysisValidation, obj, **kwargs)
