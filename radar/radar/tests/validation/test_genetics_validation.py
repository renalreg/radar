from datetime import date, datetime, timedelta

import pytest
import pytz

from radar.models.patients import Patient
from radar.models.patient_demographics import PatientDemographics
from radar.models.groups import Group, GROUP_TYPE, GroupPatient
from radar.models.genetics import Genetics
from radar.validation.core import ValidationError
from radar.validation.genetics import GeneticsValidation
from radar.tests.validation.helpers import validation_runner
from radar.exceptions import PermissionDenied


@pytest.fixture
def group():
    return Group(type=GROUP_TYPE.COHORT)


@pytest.fixture
def patient(group):
    patient = Patient()

    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)

    group_patient = GroupPatient()
    group_patient.group = group
    group_patient.patient = patient
    patient.group_patients.append(group_patient)

    return patient


@pytest.fixture
def genetics(patient, group):
    obj = Genetics()
    obj.patient = patient
    obj.group = group
    obj.date_sent = datetime(2015, 1, 2, 3, 4, 5, tzinfo=pytz.utc)
    obj.laboratory = 'Test'
    obj.reference_number = '12345'
    obj.karyotype = 1
    obj.results = 'foo\nbar\nbaz'
    obj.summary = 'hello\nworld'
    return obj


def test_valid(genetics):
    obj = valid(genetics)
    assert obj.date_sent == datetime(2015, 1, 2, 3, 4, 5, tzinfo=pytz.utc)
    assert obj.laboratory == 'Test'
    assert obj.reference_number == '12345'
    assert obj.karyotype == 1
    assert obj.results == 'foo\nbar\nbaz'
    assert obj.summary == 'hello\nworld'
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_missing(genetics):
    genetics.patient = None
    invalid(genetics)


def test_group_missing(genetics):
    genetics.group = None
    invalid(genetics)


def test_group_not_cohort(genetics):
    genetics.group.type = GROUP_TYPE.OTHER

    with pytest.raises(PermissionDenied):
        valid(genetics)


def test_date_sent_none(genetics):
    genetics.date_sent = None
    invalid(genetics)


def test_date_sent_future(genetics):
    genetics.date_sent = datetime.now(pytz.utc) + timedelta(days=1)
    invalid(genetics)


def test_date_sent_before_dob(genetics):
    genetics.date_sent = datetime(1999, 12, 31, 23, 59, 59, tzinfo=pytz.utc)
    invalid(genetics)


def test_laboratory_blank(genetics):
    genetics.laboratory = ''
    obj = valid(genetics)
    assert obj.laboratory is None


def test_reference_number_blank(genetics):
    genetics.reference_number = ''
    obj = valid(genetics)
    assert obj.reference_number is None


def test_karyotype_missing(genetics):
    genetics.karyotype = None
    obj = valid(genetics)
    assert obj.karyotype is None


def test_karyotype_invalid(genetics):
    genetics.karyotype = 99999
    invalid(genetics)


def test_results_blank(genetics):
    genetics.results = ''
    obj = valid(genetics)
    assert obj.results is None


def test_summary_blank(genetics):
    genetics.summary = ''
    obj = valid(genetics)
    assert obj.summary is None


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(Genetics, GeneticsValidation, obj, **kwargs)
