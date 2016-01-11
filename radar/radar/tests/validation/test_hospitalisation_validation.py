from datetime import date, timedelta

import pytest

from radar.models import Patient, PatientDemographics, Hospitalisation
from radar.models.groups import Group
from radar.models.source_types import SourceType, SOURCE_TYPE_RADAR
from radar.validation.core import ValidationError
from radar.validation.hospitalisations import HospitalisationValidation
from radar.tests.validation.helpers import validation_runner


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def hospitalisation(patient):
    obj = Hospitalisation()
    obj.source_group = Group()
    obj.source_type = SourceType(id=SOURCE_TYPE_RADAR)
    obj.patient = patient
    obj.date_of_admission = date(2015, 1, 1)
    obj.date_of_discharge = date(2015, 1, 2)
    obj.reason_for_admission = 'Foo'
    obj.comments = 'Bar'
    return obj


def test_valid(hospitalisation):
    obj = valid(hospitalisation)
    assert obj.date_of_admission == date(2015, 1, 1)
    assert obj.date_of_discharge == date(2015, 1, 2)
    assert obj.reason_for_admission == 'Foo'
    assert obj.comments == 'Bar'
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_missing(hospitalisation):
    hospitalisation.patient = None
    invalid(hospitalisation)


def test_source_group_missing(hospitalisation):
    hospitalisation.source_group = None
    invalid(hospitalisation)


def test_source_type_missing(hospitalisation):
    hospitalisation.source_type = None
    invalid(hospitalisation)


def test_date_of_admission_missing(hospitalisation):
    hospitalisation.date_of_admission = None
    invalid(hospitalisation)


def test_date_of_admission_before_dob(hospitalisation):
    hospitalisation.date_of_admission = date(1999, 1, 1)
    invalid(hospitalisation)


def test_date_of_admission_future(hospitalisation):
    hospitalisation.date_of_admission = date.today() + timedelta(days=1)
    invalid(hospitalisation)


def test_date_of_discharge_missing(hospitalisation):
    hospitalisation.date_of_discharge = None
    valid(hospitalisation)


def test_date_of_discharge_before_dob(hospitalisation):
    hospitalisation.date_of_discharge = date(1999, 1, 1)
    invalid(hospitalisation)


def test_date_of_discharge_future(hospitalisation):
    hospitalisation.date_of_discharge = date.today() + timedelta(days=1)
    invalid(hospitalisation)


def test_date_of_discharge_before_date_of_admission(hospitalisation):
    hospitalisation.date_of_discharge = hospitalisation.date_of_admission - timedelta(days=1)
    invalid(hospitalisation)


def test_reason_for_admission_missing(hospitalisation):
    hospitalisation.reason_for_admission = None
    valid(hospitalisation)


def test_reason_for_admission_blank(hospitalisation):
    hospitalisation.reason_for_admission = ''
    obj = valid(hospitalisation)
    assert obj.reason_for_admission is None


def test_comments_missing(hospitalisation):
    hospitalisation.comments = None
    valid(hospitalisation)


def test_comments_blank(hospitalisation):
    hospitalisation.comments = ''
    obj = valid(hospitalisation)
    assert obj.comments is None


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(Hospitalisation, HospitalisationValidation, obj, **kwargs)
