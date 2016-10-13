from datetime import date, timedelta

from cornflake.exceptions import ValidationError
import pytest

from radar.api.serializers.medications import MedicationSerializer
from radar.models.groups import Group
from radar.models.medications import Drug
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
def medication(patient):
    return {
        'source_group': Group(),
        'source_type': SOURCE_TYPE_MANUAL,
        'patient': patient,
        'from_date': date(2015, 1, 1),
        'to_date': date(2015, 1, 2),
        'drug': Drug(name='Paracetamol'),
        'drug_text': 'Paracetamol',
        'dose_quantity': 100,
        'dose_unit': 'MG',
        'frequency': 'Daily',
        'route': 'ORAL'
    }


def test_valid(medication):
    obj = valid(medication)
    assert obj.from_date == date(2015, 1, 1)
    assert obj.to_date == date(2015, 1, 2)
    assert obj.drug is not None
    assert obj.drug_text is None
    assert obj.dose_quantity == 100
    assert obj.dose_unit == 'MG'
    assert obj.frequency == 'Daily'
    assert obj.route == 'ORAL'
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_none(medication):
    medication['patient'] = None
    invalid(medication)


def test_source_group_none(medication):
    medication['source_group'] = None
    invalid(medication)


def test_source_type_none(medication):
    medication['source_type'] = None
    medication = valid(medication)
    assert medication.source_type == SOURCE_TYPE_MANUAL


def test_from_date_none(medication):
    medication['from_date'] = None
    invalid(medication)


def test_from_date_before_dob(medication):
    medication['from_date'] = date(1999, 1, 1)
    invalid(medication)


def test_from_date_future(medication):
    medication['from_date'] = date.today() + timedelta(days=1)
    invalid(medication)


def test_to_date_none(medication):
    medication['to_date'] = None
    valid(medication)


def test_to_date_before_dob(medication):
    medication['to_date'] = date(1999, 1, 1)
    invalid(medication)


def test_to_date_future(medication):
    medication['to_date'] = date.today() + timedelta(days=1)
    invalid(medication)


def test_to_date_before_from_date(medication):
    medication['to_date'] = medication['from_date'] - timedelta(days=1)
    invalid(medication)


def test_drug_none(medication):
    medication['drug'] = None
    medication = valid(medication)
    assert medication.drug_text == 'Paracetamol'


def test_drug_text_none(medication):
    medication['drug_text'] = None
    valid(medication)


def test_drug_text_empty(medication):
    medication['drug_text'] = ''
    medication = valid(medication)
    assert medication.drug_text is None


def test_drug_and_drug_text_none(medication):
    medication['drug'] = None
    medication['drug_text'] = None
    invalid(medication)


def test_dose_quantity_none(medication):
    medication['dose_quantity'] = None
    valid(medication)


def test_dose_quantity_negative(medication):
    medication['dose_quantity'] = -1
    invalid(medication)


def test_dose_unit_none(medication):
    medication['dose_quantity'] = None
    medication['dose_unit'] = None
    valid(medication)

    medication['dose_quantity'] = 1
    medication['dose_unit'] = None
    invalid(medication)


def test_dose_unit_invalid(medication):
    medication['dose_unit'] = 'FOO'
    invalid(medication)


def test_frequency_none(medication):
    medication['frequency'] = None
    valid(medication)


def test_route_none(medication):
    medication['route'] = None
    valid(medication)


def test_route_invalid(medication):
    medication['route'] = 'FOO'
    invalid(medication)


def invalid(data):
    with pytest.raises(ValidationError) as e:
        valid(data)

    return e


def valid(data):
    serializer = MedicationSerializer(data=data, context={'user': User(is_admin=True)})
    serializer.is_valid(raise_exception=True)
    return serializer.save()
