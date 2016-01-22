from datetime import date, timedelta

import pytest

from radar.models import Nephrectomy, Patient, PatientDemographics
from radar.models.groups import Group
from radar.models.source_types import SOURCE_TYPE_RADAR
from radar.validation.core import ValidationError
from radar.validation.nephrectomies import NephrectomyValidation
from radar.tests.validation.helpers import validation_runner


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def nephrectomy(patient):
    obj = Nephrectomy()
    obj.source_group = Group()
    obj.source_type = SOURCE_TYPE_RADAR
    obj.patient = patient
    obj.date = date(2015, 1, 1)
    obj.kidney_side = 'LEFT'
    obj.kidney_type = 'NATIVE'
    obj.entry_type = 'HA'
    return obj


def test_valid(nephrectomy):
    obj = valid(nephrectomy)
    assert obj.date == date(2015, 1, 1)
    assert obj.kidney_side == 'LEFT'
    assert obj.kidney_type == 'NATIVE'
    assert obj.entry_type == 'HA'
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_missing(nephrectomy):
    nephrectomy.patient = None
    invalid(nephrectomy)


def test_source_group_missing(nephrectomy):
    nephrectomy.source_group = None
    invalid(nephrectomy)


def test_source_type_missing(nephrectomy):
    nephrectomy.source_type = None
    nephrectomy = valid(nephrectomy)
    assert nephrectomy.source_type == 'RADAR'


def test_date_missing(nephrectomy):
    nephrectomy.date = None
    invalid(nephrectomy)


def test_date_before_dob(nephrectomy):
    nephrectomy.date = date(1999, 1, 1)
    invalid(nephrectomy)


def test_date_future(nephrectomy):
    nephrectomy.date = date.today() + timedelta(days=1)
    invalid(nephrectomy)


def test_kidney_side_missing(nephrectomy):
    nephrectomy.kidney_side = None
    invalid(nephrectomy)


def test_kidney_side_invalid(nephrectomy):
    nephrectomy.kidney_side = 'HELLO'
    invalid(nephrectomy)


def test_kidney_type_missing(nephrectomy):
    nephrectomy.kidney_type = None
    invalid(nephrectomy)


def test_kidney_type_invalid(nephrectomy):
    nephrectomy.kidney_type = 'HELLO'
    invalid(nephrectomy)


def test_entry_type_missing(nephrectomy):
    nephrectomy.entry_type = None
    invalid(nephrectomy)


def test_entry_type_invalid(nephrectomy):
    nephrectomy.entry_type = 'HELLO'
    invalid(nephrectomy)


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(Nephrectomy, NephrectomyValidation, obj, **kwargs)
