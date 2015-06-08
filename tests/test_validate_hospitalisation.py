from datetime import date, timedelta

import pytest

from radar.lib.validation.core import ErrorHandler
from radar.lib.validation.hospitalisations import validate_hospitalisation
from radar.models import Patient, PatientDemographics, Plasmapheresis, PlasmapheresisResponse


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.demographics_list.append(patient_demographics)
    return patient


@pytest.fixture
def hospitalisation(patient):
    hospitalisation = Plasmapheresis()
    hospitalisation.patient = patient
    hospitalisation.date_of_admission = date(2015, 1, 1)
    hospitalisation.date_of_discharge = date(2015, 1, 2)
    return hospitalisation


@pytest.fixture
def errors():
    errors = ErrorHandler()
    return errors


def test_hospitalisation_valid(errors, hospitalisation):
    validate_hospitalisation(errors, hospitalisation)
    assert errors.is_valid()


def test_hospitalisation_date_of_admission_missing(errors, hospitalisation):
    hospitalisation.date_of_admission = None
    validate_hospitalisation(errors, hospitalisation)
    assert not errors.is_valid()


def test_hospitalisation_date_of_admission_before_dob(errors, hospitalisation):
    hospitalisation.date_of_admission = date(1999, 1, 1)
    validate_hospitalisation(errors, hospitalisation)
    assert not errors.is_valid()


def test_hospitalisation_date_of_admission_future(errors, hospitalisation):
    hospitalisation.date_of_admission = date.today() + timedelta(days=1)
    validate_hospitalisation(errors, hospitalisation)
    assert not errors.is_valid()


def test_hospitalisation_date_of_discharge_missing(errors, hospitalisation):
    hospitalisation.date_of_discharge = None
    validate_hospitalisation(errors, hospitalisation)
    assert errors.is_valid()


def test_hospitalisation_date_of_discharge_before_dob(errors, hospitalisation):
    hospitalisation.date_of_discharge = date(1999, 1, 1)
    validate_hospitalisation(errors, hospitalisation)
    assert not errors.is_valid()


def test_hospitalisation_date_of_discharge_future(errors, hospitalisation):
    hospitalisation.date_of_discharge = date.today() + timedelta(days=1)
    validate_hospitalisation(errors, hospitalisation)
    assert not errors.is_valid()


def test_hospitalisation_date_of_discharge_before_date_of_admission(errors, hospitalisation):
    hospitalisation.date_of_discharge = hospitalisation.date_of_admission - timedelta(days=1)
    validate_hospitalisation(errors, hospitalisation)
    assert not errors.is_valid()
