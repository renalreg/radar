from datetime import date, timedelta

from cornflake.exceptions import ValidationError
import pytest

from radar.api.serializers.transplants import TransplantSerializer
from radar.models.groups import Group
from radar.models.patient_demographics import PatientDemographics
from radar.models.patients import Patient
from radar.models.source_types import SOURCE_TYPE_MANUAL
from radar.models.users import User


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def transplant(patient):
    return {
        'source_group': Group(),
        'source_type': SOURCE_TYPE_MANUAL,
        'patient': patient,
        'date': date(2015, 1, 1),
        'modality': 29,
        'date_of_failure': date(2015, 1, 2)
    }


@pytest.fixture
def transplant1(patient):
    return {
        'source_group': Group(),
        'source_type': SOURCE_TYPE_MANUAL,
        'patient': patient,
        'date': date(2015, 1, 1),
        'modality': 29,
        'date_of_failure': date(2015, 1, 2),
        'recurrence': True,
    }



def test_valid(transplant):
    obj = valid(transplant)
    assert obj.date == date(2015, 1, 1)
    assert obj.modality == 29
    assert obj.date_of_failure == date(2015, 1, 2)
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_recurrence_is_set(transplant1):
    obj = valid(transplant1)
    assert obj.recurrence


def test_patient_none(transplant):
    transplant['patient'] = None
    invalid(transplant)


def test_source_group_none(transplant):
    transplant['source_group'] = None
    invalid(transplant)


def test_source_type_none(transplant):
    transplant['source_type'] = None
    obj = valid(transplant)
    assert obj.source_type == SOURCE_TYPE_MANUAL


def test_date_none(transplant):
    transplant['date'] = None
    invalid(transplant)


def test_date_before_dob(transplant):
    transplant['date'] = date(1999, 1, 1)
    invalid(transplant)


def test_date_future(transplant):
    transplant['date'] = date.today() + timedelta(days=1)
    invalid(transplant)


def test_modality_none(transplant):
    transplant['modality'] = None
    invalid(transplant)


def test_modality_invalid(transplant):
    transplant['modality'] = 0
    invalid(transplant)


def test_date_of_failure_none(transplant):
    transplant['date_of_failure'] = None
    valid(transplant)


def test_date_of_failure_before_dob(transplant):
    transplant['date_of_failure'] = date(1999, 1, 1)
    invalid(transplant)


def test_date_of_failure_future(transplant):
    transplant['date_of_failure'] = date.today() + timedelta(days=1)
    invalid(transplant)


def test_date_of_failure_before_transplant_date(transplant):
    transplant['date_of_failure'] = transplant['date'] - timedelta(days=1)
    invalid(transplant)


def invalid(data):
    with pytest.raises(ValidationError) as e:
        valid(data)

    return e


def valid(data):
    serializer = TransplantSerializer(data=data, context={'user': User(is_admin=True)})
    serializer.is_valid(raise_exception=True)
    return serializer.save()
