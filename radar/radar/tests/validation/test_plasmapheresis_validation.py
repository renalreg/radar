from datetime import date, timedelta

import pytest

from radar.models import Patient, PatientDemographics, Plasmapheresis
from radar.models.groups import Group
from radar.models.source_types import SourceType, SOURCE_TYPE_RADAR
from radar.validation.core import ValidationError
from radar.validation.plasmapheresis import PlasmapheresisValidation
from radar.tests.validation.helpers import validation_runner


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def plasmapheresis(patient):
    obj = Plasmapheresis()
    obj.source_group = Group()
    obj.source_type = SourceType(id=SOURCE_TYPE_RADAR)
    obj.patient = patient
    obj.from_date = date(2015, 1, 1)
    obj.to_date = date(2015, 1, 2)
    obj.no_of_exchanges = '1/1D'
    obj.response = 'COMPLETE'
    return obj


def test_valid(plasmapheresis):
    obj = valid(plasmapheresis)
    assert obj.from_date == date(2015, 1, 1)
    assert obj.to_date == date(2015, 1, 2)
    assert obj.no_of_exchanges == '1/1D'
    assert obj.response == 'COMPLETE'
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_missing(plasmapheresis):
    plasmapheresis.patient = None
    invalid(plasmapheresis)


def test_source_group_missing(plasmapheresis):
    plasmapheresis.source_group = None
    invalid(plasmapheresis)


def test_source_type_missing(plasmapheresis):
    plasmapheresis.source_type = None
    invalid(plasmapheresis)


def test_from_date_missing(plasmapheresis):
    plasmapheresis.from_date = None
    invalid(plasmapheresis)


def test_from_date_before_dob(plasmapheresis):
    plasmapheresis.from_date = date(1999, 1, 1)
    invalid(plasmapheresis)


def test_from_date_future(plasmapheresis):
    plasmapheresis.from_date = date.today() + timedelta(days=1)
    invalid(plasmapheresis)


def test_to_date_missing(plasmapheresis):
    plasmapheresis.to_date = None
    valid(plasmapheresis)


def test_to_date_before_dob(plasmapheresis):
    plasmapheresis.to_date = date(1999, 1, 1)
    invalid(plasmapheresis)


def test_to_date_future(plasmapheresis):
    plasmapheresis.to_date = date.today() + timedelta(days=1)
    invalid(plasmapheresis)


def test_to_date_before_from_date(plasmapheresis):
    plasmapheresis.to_date = plasmapheresis.from_date - timedelta(days=1)
    invalid(plasmapheresis)


def test_no_of_exchanges_missing(plasmapheresis):
    plasmapheresis.no_of_exchanges = None
    valid(plasmapheresis)


def test_no_of_exchanges_invalid(plasmapheresis):
    plasmapheresis.no_of_exchanges = 'FOO'
    invalid(plasmapheresis)


def test_response_missing(plasmapheresis):
    plasmapheresis.response = None
    valid(plasmapheresis)


def test_response_invalid(plasmapheresis):
    plasmapheresis.response = 'FOO'
    invalid(plasmapheresis)


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(Plasmapheresis, PlasmapheresisValidation, obj, **kwargs)
