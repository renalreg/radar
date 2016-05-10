from datetime import date

import pytest
from cornflake.exceptions import ValidationError

from radar.api.serializers.pathology import PathologySerializer
from radar.models.groups import Group
from radar.models.patient_demographics import PatientDemographics
from radar.models.patients import Patient
from radar.models.source_types import SOURCE_TYPE_RADAR
from radar.models.users import User


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def pathology(patient):
    return {
        'source_group': Group(),
        'source_type': SOURCE_TYPE_RADAR,
        'patient': patient,
        'date': date(2015, 1, 1),
        'kidney_type': 'NATIVE',
        'kidney_side': 'RIGHT',
        'reference_number': '12345',
        'histological_summary': 'foo bar baz'
    }


def test_valid(pathology):
    obj = valid(pathology)
    assert obj.date == date(2015, 1, 1)
    assert obj.kidney_type == 'NATIVE'
    assert obj.kidney_side == 'RIGHT'
    assert obj.reference_number == '12345'
    assert obj.histological_summary == 'foo bar baz'


def test_patient_none(pathology):
    pathology['patient'] = None
    invalid(pathology)


def test_source_group_none(pathology):
    pathology['source_group'] = None
    invalid(pathology)


def test_source_type_none(pathology):
    pathology['source_type'] = None
    pathology = valid(pathology)
    assert pathology.source_type == 'RADAR'


def test_kidney_type_none(pathology):
    pathology['kidney_type'] = None
    valid(pathology)


def test_kidney_type_blank(pathology):
    pathology['kidney_type'] = ''
    invalid(pathology)


def test_kidney_type_native(pathology):
    pathology['kidney_type'] = 'NATIVE'
    obj = valid(pathology)
    assert obj.kidney_type == 'NATIVE'


def test_kidney_type_transplant(pathology):
    pathology['kidney_type'] = 'TRANSPLANT'
    obj = valid(pathology)
    assert obj.kidney_type == 'TRANSPLANT'


def test_kidney_type_invalid(pathology):
    pathology['kidney_type'] = 'HELLO'
    invalid(pathology)


def test_kidney_side_none(pathology):
    pathology['kidney_side'] = None
    valid(pathology)


def test_kidney_side_blank(pathology):
    pathology['kidney_side'] = ''
    invalid(pathology)


def test_kidney_side_left(pathology):
    pathology['kidney_side'] = 'LEFT'
    obj = valid(pathology)
    assert obj.kidney_side == 'LEFT'


def test_kidney_side_right(pathology):
    pathology['kidney_side'] = 'RIGHT'
    obj = valid(pathology)
    assert obj.kidney_side == 'RIGHT'


def test_kidney_side_invalid(pathology):
    pathology['kidney_side'] = 'HELLO'
    invalid(pathology)


def test_reference_number_none(pathology):
    pathology['reference_number'] = None
    valid(pathology)


def test_reference_number_blank(pathology):
    pathology['reference_number'] = ''
    valid(pathology)


def test_histological_summary_none(pathology):
    pathology['histological_summary'] = None
    obj = valid(pathology)
    assert obj.histological_summary is None


def test_histological_summary_blank(pathology):
    pathology['histological_summary'] = ''
    obj = valid(pathology)
    assert obj.histological_summary is None


def invalid(data):
    with pytest.raises(ValidationError) as e:
        valid(data)

    return e


def valid(data):
    serializer = PathologySerializer(data=data, context={'user': User(is_admin=True)})
    serializer.is_valid(raise_exception=True)
    return serializer.save()
