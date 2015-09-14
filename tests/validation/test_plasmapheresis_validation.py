from datetime import date, timedelta

import pytest

from radar.lib.models import Patient, PatientDemographics, Plasmapheresis, DataSource, User
from radar.lib.validation.core import ValidationError
from radar.lib.validation.plasmapheresis import PlasmapheresisValidation


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def plasmapheresis(patient):
    plasmapheresis = Plasmapheresis()
    plasmapheresis.data_source = DataSource()
    plasmapheresis.patient = patient
    plasmapheresis.from_date = date(2015, 1, 1)
    plasmapheresis.to_date = date(2015, 1, 2)
    plasmapheresis.no_of_exchanges = 3
    plasmapheresis.response = 'HELLO'  # TODO
    return plasmapheresis


def test_valid(plasmapheresis):
    obj = valid(plasmapheresis)
    assert obj.from_date == date(2015, 1, 1)
    assert obj.to_date == date(2015, 1, 2)
    assert obj.no_of_exchanges == 3
    assert obj.response == 'HELLO'


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
    invalid(plasmapheresis)


def test_no_of_exchanges_zero(plasmapheresis):
    plasmapheresis.no_of_exchanges = 0
    valid(plasmapheresis)


def test_response_missing(plasmapheresis):
    plasmapheresis.response = None
    invalid(plasmapheresis)


def valid(plasmapheresis):
    return validate(plasmapheresis)


def invalid(plasmapheresis):
    with pytest.raises(ValidationError):
        validate(plasmapheresis)


def validate(plasmapheresis):
    validation = PlasmapheresisValidation()
    ctx = {'user': User(is_admin=True)}
    validation.before_update(ctx, Plasmapheresis())
    old_obj = validation.clone(plasmapheresis)
    obj = validation.after_update(ctx, old_obj, plasmapheresis)
    return obj
