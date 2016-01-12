from datetime import date, timedelta

import pytest

from radar.models import Medication, Patient, PatientDemographics
from radar.models.groups import Group
from radar.models.source_types import SOURCE_TYPE_RADAR
from radar.validation.core import ValidationError
from radar.validation.medications import MedicationValidation
from radar.tests.validation.helpers import validation_runner


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def medication(patient):
    obj = Medication()
    obj.source_group = Group()
    obj.source_type = SOURCE_TYPE_RADAR
    obj.patient = patient
    obj.from_date = date(2015, 1, 1)
    obj.to_date = date(2015, 1, 2)
    obj.name = 'Paracetamol'
    obj.dose_quantity = 100
    obj.dose_unit = 'MG'
    obj.frequency = 'DAILY'
    obj.route = 'ORAL'
    return obj


def test_valid(medication):
    obj = valid(medication)
    assert obj.from_date == date(2015, 1, 1)
    assert obj.to_date == date(2015, 1, 2)
    assert obj.name == 'Paracetamol'
    assert obj.dose_quantity == 100
    assert obj.dose_unit == 'MG'
    assert obj.frequency == 'DAILY'
    assert obj.route == 'ORAL'
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_missing(medication):
    medication.patient = None
    invalid(medication)


def test_source_group_missing(medication):
    medication.source_group = None
    invalid(medication)


def test_source_type_missing(medication):
    medication.source_type = None
    medication = valid(medication)
    assert medication.source_type == 'RADAR'


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
    valid(medication)


def test_dose_quantity_negative(medication):
    medication.dose_quantity = -1
    invalid(medication)


def test_dose_unit_missing(medication):
    medication.dose_quantity = None
    medication.dose_unit = None
    valid(medication)

    medication.dose_quantity = 1
    medication.dose_unit = None
    invalid(medication)


def test_dose_unit_invalid(medication):
    medication.dose_unit = 'FOO'
    invalid(medication)


def test_frequency_missing(medication):
    medication.frequency = None
    valid(medication)


def test_frequency_invalid(medication):
    medication.frequency = 'FOO'
    invalid(medication)


def test_route_missing(medication):
    medication.route = None
    valid(medication)


def test_route_invalid(medication):
    medication.route = 'FOO'
    invalid(medication)


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(Medication, MedicationValidation, obj, **kwargs)
