from datetime import date, timedelta

import pytest

from radar.models import Patient, PatientDemographics, DataSource, Comorbidity, Disorder
from radar.validation.comorbidities import ComorbidityValidation
from radar.validation.core import ValidationError
from radar.tests.helpers.validation import validation_runner


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def comorbidity(patient):
    obj = Comorbidity()
    obj.data_source = DataSource()
    obj.patient = patient
    obj.from_date = date(2015, 1, 1)
    obj.to_date = date(2015, 1, 2)
    obj.disorder = Disorder(id=1)
    return obj


def test_valid(comorbidity):
    disorder = comorbidity.disorder
    obj = valid(comorbidity)
    assert obj.from_date == date(2015, 1, 1)
    assert obj.to_date == date(2015, 1, 2)
    assert obj.disorder == disorder
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_missing(comorbidity):
    comorbidity.patient = None
    invalid(comorbidity)


def test_data_source_missing(comorbidity):
    comorbidity.data_source = None
    invalid(comorbidity)


def test_from_date_missing(comorbidity):
    comorbidity.from_date = None
    invalid(comorbidity)


def test_from_date_before_dob(comorbidity):
    comorbidity.from_date = date(1999, 1, 1)
    invalid(comorbidity)


def test_from_date_future(comorbidity):
    comorbidity.from_date = date.today() + timedelta(days=1)
    invalid(comorbidity)


def test_to_date_missing(comorbidity):
    comorbidity.to_date = None
    valid(comorbidity)


def test_to_date_before_dob(comorbidity):
    comorbidity.to_date = date(1999, 1, 1)
    invalid(comorbidity)


def test_to_date_future(comorbidity):
    comorbidity.to_date = date.today() + timedelta(days=1)
    invalid(comorbidity)


def test_to_date_before_from_date(comorbidity):
    comorbidity.to_date = comorbidity.from_date - timedelta(days=1)
    invalid(comorbidity)


def test_disorder_missing(comorbidity):
    comorbidity.disorder = None
    invalid(comorbidity)


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(Comorbidity, ComorbidityValidation, obj, **kwargs)
