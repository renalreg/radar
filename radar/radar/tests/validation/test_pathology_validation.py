from datetime import date

import pytest

from radar.models import Patient, PatientDemographics, Pathology
from radar.models.groups import Group
from radar.models.source_types import SourceType, SOURCE_TYPE_RADAR
from radar.validation.core import ValidationError
from radar.validation.pathology import PathologyValidation
from radar.tests.validation.helpers import validation_runner


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def pathology(patient):
    obj = Pathology()
    obj.source_group = Group()
    obj.source_type = SourceType(id=SOURCE_TYPE_RADAR)
    obj.patient = patient
    obj.date = date(2015, 1, 1)
    obj.kidney_type = 'NATIVE'
    obj.kidney_side = 'RIGHT'
    obj.reference_number = '12345'
    obj.histological_summary = 'foo bar baz'
    return obj


def test_valid(pathology):
    obj = valid(pathology)
    assert obj.date == date(2015, 1, 1)
    assert obj.kidney_type == 'NATIVE'
    assert obj.kidney_side == 'RIGHT'
    assert obj.reference_number == '12345'
    assert obj.histological_summary == 'foo bar baz'


def test_patient_missing(pathology):
    pathology.patient = None
    invalid(pathology)


def test_source_group_missing(pathology):
    pathology.source_group = None
    pathology = valid(pathology)
    assert pathology.source_type.id == 'RADAR'


def test_source_type_missing(pathology):
    pathology.source_type = None
    pathology = valid(pathology)
    assert pathology.source_type.id == 'RADAR'


def test_kidney_type_missing(pathology):
    pathology.kidney_type = None
    invalid(pathology)


def test_kidney_type_blank(pathology):
    pathology.kidney_type = ''
    invalid(pathology)


def test_kidney_type_native(pathology):
    pathology.kidney_type = 'NATIVE'
    obj = valid(pathology)
    assert obj.kidney_type == 'NATIVE'


def test_kidney_type_transplant(pathology):
    pathology.kidney_type = 'TRANSPLANT'
    obj = valid(pathology)
    assert obj.kidney_type == 'TRANSPLANT'


def test_kidney_type_invalid(pathology):
    pathology.kidney_type = 'HELLO'
    invalid(pathology)


def test_kidney_side_missing(pathology):
    pathology.kidney_side = None
    invalid(pathology)


def test_kidney_side_blank(pathology):
    pathology.kidney_side = ''
    invalid(pathology)


def test_kidney_side_left(pathology):
    pathology.kidney_side = 'LEFT'
    obj = valid(pathology)
    assert obj.kidney_side == 'LEFT'


def test_kidney_side_right(pathology):
    pathology.kidney_side = 'RIGHT'
    obj = valid(pathology)
    assert obj.kidney_side == 'RIGHT'


def test_kidney_side_invalid(pathology):
    pathology.kidney_side = 'HELLO'
    invalid(pathology)


def test_reference_number_missing(pathology):
    pathology.reference_number = None
    valid(pathology)


def test_reference_number_blank(pathology):
    pathology.reference_number = ''
    valid(pathology)


def test_histological_summary_missing(pathology):
    pathology.histological_summary = None
    obj = valid(pathology)
    assert obj.histological_summary is None


def test_histological_summary_blank(pathology):
    pathology.histological_summary = ''
    obj = valid(pathology)
    assert obj.histological_summary is None


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(Pathology, PathologyValidation, obj, **kwargs)
