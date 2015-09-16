from datetime import date, datetime, timedelta

import pytest
import pytz

from radar.lib.models import Patient, PatientDemographics, Cohort, Genetics
from radar.lib.validation.core import ValidationError
from radar.lib.validation.genetics import GeneticsValidation
from utils import validation_runner


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def genetics(patient):
    obj = Genetics()
    obj.patient = patient
    obj.cohort = Cohort(id=1)
    obj.sample_sent = True
    obj.sample_sent_date = datetime(2015, 1, 2, 3, 4, 5, tzinfo=pytz.UTC)
    obj.laboratory = 'Test'
    obj.laboratory_reference_number = '12345'
    obj.results = 'foo\nbar\nbaz'
    return obj


def test_valid(genetics):
    obj = valid(genetics)
    assert obj.sample_sent is True
    assert obj.sample_sent_date == datetime(2015, 1, 2, 3, 4, 5, tzinfo=pytz.UTC)
    assert obj.laboratory == 'Test'
    assert obj.laboratory_reference_number == '12345'
    assert obj.results == 'foo\nbar\nbaz'
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_missing(genetics):
    genetics.patient = None
    invalid(genetics)


def test_cohort_missing(genetics):
    genetics.cohort = None
    invalid(genetics)


def test_sample_not_sent(genetics):
    genetics.sample_sent = False
    obj = valid(genetics)
    assert obj.sample_sent_date is None
    assert obj.laboratory is None
    assert obj.laboratory_reference_number is None
    assert obj.results is None


def test_sample_sent_date_none(genetics):
    genetics.sample_sent_date = None
    invalid(genetics)


def test_sample_sent_date_future(genetics):
    genetics.sample_sent_date = datetime.now(pytz.UTC) + timedelta(days=1)
    invalid(genetics)


def test_sample_sent_date_before_dob(genetics):
    genetics.sample_sent_date = datetime(1999, 12, 31, 23, 59, 59, tzinfo=pytz.UTC)
    invalid(genetics)


def test_laboratory_blank(genetics):
    genetics.laboratory = ''
    obj = valid(genetics)
    assert obj.laboratory is None


def test_laboratory_reference_number_blank(genetics):
    genetics.laboratory_reference_number = ''
    obj = valid(genetics)
    assert obj.laboratory_reference_number is None


def test_results_blank(genetics):
    genetics.results = ''
    obj = valid(genetics)
    assert obj.results is None


def valid(obj, **kwargs):
    return validate(obj, **kwargs)


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        validate(obj, **kwargs)

    return e


def validate(obj, **kwargs):
    return validation_runner(Genetics, GeneticsValidation, obj, **kwargs)
