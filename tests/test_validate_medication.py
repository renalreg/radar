from datetime import date, timedelta

import pytest

from radar.lib.validation.core import ErrorHandler
from radar.lib.validation.medications import validate_medication
from radar.models import Medication, MedicationDoseUnit, MedicationRoute, MedicationFrequency, Patient, \
    PatientDemographics


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.demographics_list.append(patient_demographics)
    return patient


@pytest.fixture
def medication(patient):
    medication = Medication()
    medication.patient = patient
    medication.from_date = date(2015, 1, 1)
    medication.to_date = date(2015, 1, 2)
    medication.name = 'Paracetamol'
    medication.dose_quantity = 100
    medication.dose_unit = MedicationDoseUnit(id='mg')
    medication.frequency = MedicationFrequency(id='daily')
    medication.route = MedicationRoute(id='oral')
    return medication


@pytest.fixture
def errors():
    errors = ErrorHandler()
    return errors


def test_medication_valid(errors, medication):
    validate_medication(errors, medication)
    assert errors.is_valid()


def test_medication_from_date_missing(errors, medication):
    medication.from_date = None
    validate_medication(errors, medication)
    assert not errors.is_valid()


def test_medication_from_date_before_dob(errors, medication):
    medication.from_date = date(1999, 1, 1)
    validate_medication(errors, medication)
    assert not errors.is_valid()


def test_medication_from_date_future(errors, medication):
    medication.from_date = date.today() + timedelta(days=1)
    validate_medication(errors, medication)
    assert not errors.is_valid()


def test_medication_to_date_missing(errors, medication):
    medication.to_date = None
    validate_medication(errors, medication)
    assert errors.is_valid()


def test_medication_to_date_before_dob(errors, medication):
    medication.to_date = date(1999, 1, 1)
    validate_medication(errors, medication)
    assert not errors.is_valid()


def test_medication_to_date_future(errors, medication):
    medication.to_date = date.today() + timedelta(days=1)
    validate_medication(errors, medication)
    assert not errors.is_valid()


def test_medication_to_date_before_from_date(errors, medication):
    medication.to_date = medication.from_date - timedelta(days=1)
    validate_medication(errors, medication)
    assert not errors.is_valid()


def test_medication_name_missing(errors, medication):
    medication.name = None
    validate_medication(errors, medication)
    assert not errors.is_valid()


def test_medication_name_empty(errors, medication):
    medication.name = ''
    validate_medication(errors, medication)
    assert not errors.is_valid()


def test_medication_dose_quantity_missing(errors, medication):
    medication.dose_quantity = None
    validate_medication(errors, medication)
    assert not errors.is_valid()


def test_medication_dose_quantity_negative(errors, medication):
    medication.dose_quantity = -1
    validate_medication(errors, medication)
    assert not errors.is_valid()


def test_medication_dose_unit_missing(errors, medication):
    medication.dose_quantity = None
    validate_medication(errors, medication)
    assert not errors.is_valid()


def test_medication_frequency_missing(errors, medication):
    medication.frequency = None
    validate_medication(errors, medication)
    assert not errors.is_valid()


def test_medication_route_missing(errors, medication):
    medication.route = None
    validate_medication(errors, medication)
    assert not errors.is_valid()
