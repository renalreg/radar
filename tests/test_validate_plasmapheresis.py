from datetime import date, timedelta

import pytest

from radar.lib.validation.core import ErrorHandler
from radar.lib.validation.plasmapheresis import validate_plasmapheresis
from radar.models import Patient, PatientDemographics, Plasmapheresis, PlasmapheresisResponse


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.demographics_list.append(patient_demographics)
    return patient


@pytest.fixture
def plasmapheresis(patient):
    plasmapheresis = Plasmapheresis()
    plasmapheresis.patient = patient
    plasmapheresis.from_date = date(2015, 1, 1)
    plasmapheresis.to_date = date(2015, 1, 2)
    plasmapheresis.no_of_exchanges = 3
    plasmapheresis.response = PlasmapheresisResponse(id=1)
    return plasmapheresis


@pytest.fixture
def errors():
    errors = ErrorHandler()
    return errors


def test_plasmapheresis_valid(errors, plasmapheresis):
    validate_plasmapheresis(errors, plasmapheresis)
    assert errors.is_valid()


def test_plasmapheresis_from_date_missing(errors, plasmapheresis):
    plasmapheresis.from_date = None
    validate_plasmapheresis(errors, plasmapheresis)
    assert not errors.is_valid()


def test_plasmapheresis_from_date_before_dob(errors, plasmapheresis):
    plasmapheresis.from_date = date(1999, 1, 1)
    validate_plasmapheresis(errors, plasmapheresis)
    assert not errors.is_valid()


def test_plasmapheresis_from_date_future(errors, plasmapheresis):
    plasmapheresis.from_date = date.today() + timedelta(days=1)
    validate_plasmapheresis(errors, plasmapheresis)
    assert not errors.is_valid()


def test_plasmapheresis_to_date_missing(errors, plasmapheresis):
    plasmapheresis.to_date = None
    validate_plasmapheresis(errors, plasmapheresis)
    assert errors.is_valid()


def test_plasmapheresis_to_date_before_dob(errors, plasmapheresis):
    plasmapheresis.to_date = date(1999, 1, 1)
    validate_plasmapheresis(errors, plasmapheresis)
    assert not errors.is_valid()


def test_plasmapheresis_to_date_future(errors, plasmapheresis):
    plasmapheresis.to_date = date.today() + timedelta(days=1)
    validate_plasmapheresis(errors, plasmapheresis)
    assert not errors.is_valid()


def test_plasmapheresis_to_date_before_from_date(errors, plasmapheresis):
    plasmapheresis.to_date = plasmapheresis.from_date - timedelta(days=1)
    validate_plasmapheresis(errors, plasmapheresis)
    assert not errors.is_valid()


def test_plasmapheresis_no_of_exchanges_missing(errors, plasmapheresis):
    plasmapheresis.no_of_exchanges = None
    validate_plasmapheresis(errors, plasmapheresis)
    assert not errors.is_valid()


def test_plasmapheresis_no_of_exchanges_zero(errors, plasmapheresis):
    plasmapheresis.no_of_exchanges = 0
    validate_plasmapheresis(errors, plasmapheresis)
    assert errors.is_valid()


def test_plasmapheresis_response_missing(errors, plasmapheresis):
    plasmapheresis.response = None
    validate_plasmapheresis(errors, plasmapheresis)
    assert not errors.is_valid()
