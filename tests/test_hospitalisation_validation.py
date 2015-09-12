from datetime import date, timedelta

import pytest

from radar.lib.models import Patient, PatientDemographics, Hospitalisation, DataSource, User
from radar.lib.validation.core import ValidationError
from radar.lib.validation.hospitalisations import HospitalisationValidation


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def hospitalisation(patient):
    hospitalisation = Hospitalisation()
    hospitalisation.data_source = DataSource()
    hospitalisation.patient = patient
    hospitalisation.date_of_admission = date(2015, 1, 1)
    hospitalisation.date_of_discharge = date(2015, 1, 2)
    return hospitalisation


def test_hospitalisation_valid(hospitalisation):
    valid(hospitalisation)


def test_hospitalisation_date_of_admission_missing(hospitalisation):
    hospitalisation.date_of_admission = None
    invalid(hospitalisation)


def test_hospitalisation_date_of_admission_before_dob(hospitalisation):
    hospitalisation.date_of_admission = date(1999, 1, 1)
    invalid(hospitalisation)


def test_hospitalisation_date_of_admission_future(hospitalisation):
    hospitalisation.date_of_admission = date.today() + timedelta(days=1)
    invalid(hospitalisation)


def test_hospitalisation_date_of_discharge_missing(hospitalisation):
    hospitalisation.date_of_discharge = None
    valid(hospitalisation)


def test_hospitalisation_date_of_discharge_before_dob(hospitalisation):
    hospitalisation.date_of_discharge = date(1999, 1, 1)
    invalid(hospitalisation)


def test_hospitalisation_date_of_discharge_future(hospitalisation):
    hospitalisation.date_of_discharge = date.today() + timedelta(days=1)
    invalid(hospitalisation)


def test_hospitalisation_date_of_discharge_before_date_of_admission(hospitalisation):
    hospitalisation.date_of_discharge = hospitalisation.date_of_admission - timedelta(days=1)
    invalid(hospitalisation)


def valid(hospitalisation):
    validate(hospitalisation)


def invalid(hospitalisation):
    with pytest.raises(ValidationError):
        validate(hospitalisation)


def validate(hospitalisation):
    validation = HospitalisationValidation()
    ctx = {'user': User(is_admin=True)}
    validation.before_update(ctx, Hospitalisation())
    old_obj = validation.clone(hospitalisation)
    validation.after_update(ctx, old_obj, hospitalisation)
