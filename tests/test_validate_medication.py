from datetime import date, timedelta
import pytest
from radar.lib.validation.core import ErrorHandler
from radar.lib.validation.medications import validate_medication
from radar.models import Medication, MedicationDoseUnit, MedicationRoute, MedicationFrequency


@pytest.fixture
def medication():
    medication = Medication()
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


def test_medication_missing_from_date(errors, medication):
    medication.from_date = None
    validate_medication(errors, medication)
    assert not errors.is_valid()


def test_medication_missing_to_date(errors, medication):
    medication.to_date = None
    validate_medication(errors, medication)
    assert errors.is_valid()


def test_medication_to_date_before_from_date(errors, medication):
    medication.to_date = medication.from_date - timedelta(days=1)
    validate_medication(errors, medication)
    assert not errors.is_valid()


def test_medication_missing_name(errors, medication):
    medication.name = None
    validate_medication(errors, medication)
    assert not errors.is_valid()


def test_medication_empty_name(errors, medication):
    medication.name = ''
    validate_medication(errors, medication)
    assert not errors.is_valid()


def test_medication_missing_dose_quantity(errors, medication):
    medication.dose_quantity = None
    validate_medication(errors, medication)
    assert not errors.is_valid()


def test_medication_negative_dose_quantity(errors, medication):
    medication.dose_quantity = -1
    validate_medication(errors, medication)
    assert not errors.is_valid()


def test_medication_missing_dose_unit(errors, medication):
    medication.dose_quantity = None
    validate_medication(errors, medication)
    assert not errors.is_valid()


def test_medication_missing_frequency(errors, medication):
    medication.frequency = None
    validate_medication(errors, medication)
    assert not errors.is_valid()


def test_medication_missing_route(errors, medication):
    medication.route = None
    validate_medication(errors, medication)
    assert not errors.is_valid()
