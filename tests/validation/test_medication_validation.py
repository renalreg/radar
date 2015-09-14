from datetime import date, timedelta

import pytest

from radar.lib.models import Medication, Patient, \
    PatientDemographics, User, DataSource
from radar.lib.validation.core import ValidationError
from radar.lib.validation.medications import MedicationValidation


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def medication(patient):
    medication = Medication()
    medication.data_source = DataSource()
    medication.patient = patient
    medication.from_date = date(2015, 1, 1)
    medication.to_date = date(2015, 1, 2)
    medication.name = 'Paracetamol'
    medication.dose_quantity = 100
    medication.dose_unit = 'MG'
    medication.frequency = 'DAILY'
    medication.route = 'ORAL'
    return medication


def test_valid(medication):
    obj = valid(medication)
    assert obj.from_date == date(2015, 1, 1)
    assert obj.to_date == date(2015, 1, 2)
    assert obj.name == 'Paracetamol'
    assert obj.dose_quantity == 100
    assert obj.dose_unit == 'MG'
    assert obj.frequency == 'DAILY'
    assert obj.route == 'ORAL'


def test_from_date_missing(medication):
    medication.from_date = None
    invalid(medication)


def test_from_date_before_dob(medication):
    medication.from_date = date(1999, 1, 1)
    invalid(medication)


def test_from_date_future(medication):
    medication.from_date = date.today() + timedelta(days=1)
    invalid(medication)


def test_to_date_missing(medication):
    medication.to_date = None
    valid(medication)


def test_to_date_before_dob(medication):
    medication.to_date = date(1999, 1, 1)
    invalid(medication)


def test_to_date_future(medication):
    medication.to_date = date.today() + timedelta(days=1)
    invalid(medication)


def test_to_date_before_from_date(medication):
    medication.to_date = medication.from_date - timedelta(days=1)
    invalid(medication)


def test_name_missing(medication):
    medication.name = None
    invalid(medication)


def test_name_empty(medication):
    medication.name = ''
    invalid(medication)


def test_dose_quantity_missing(medication):
    medication.dose_quantity = None
    invalid(medication)


def test_dose_quantity_negative(medication):
    medication.dose_quantity = -1
    invalid(medication)


def test_dose_unit_missing(medication):
    medication.dose_quantity = None
    invalid(medication)


def test_dose_unit_invalid(medication):
    medication.dose_unit = 'FOO'
    invalid(medication)


def test_frequency_missing(medication):
    medication.frequency = None
    invalid(medication)


def test_frequency_invalid(medication):
    medication.frequency = 'FOO'
    invalid(medication)


def test_route_missing(medication):
    medication.route = None
    invalid(medication)


def test_route_invalid(medication):
    medication.route = 'FOO'
    invalid(medication)


def valid(medication):
    return validate(medication)


def invalid(medication):
    with pytest.raises(ValidationError):
        validate(medication)


def validate(medication):
    validation = MedicationValidation()
    ctx = {'user': User(is_admin=True)}
    validation.before_update(ctx, Medication())
    old_obj = validation.clone(medication)
    obj = validation.after_update(ctx, old_obj, medication)
    return obj
