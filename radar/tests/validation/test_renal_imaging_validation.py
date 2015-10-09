from datetime import date, timedelta

import pytest

from radar.models import RenalImaging, DataSource, Patient, PatientDemographics
from radar.validation.core import ValidationError
from radar.validation.renal_imaging import RenalImagingValidation
from utils import validation_runner


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def renal_imaging(patient):
    obj = RenalImaging()
    obj.data_source = DataSource()
    obj.patient = patient
    obj.date = date(2015, 1, 1)
    obj.imaging_type = 'USS'
    obj.right_present = True
    obj.right_type = 'NATURAL'
    obj.right_length = 10
    obj.right_volume = 50
    obj.right_cysts = True
    obj.right_calcification = True
    obj.right_nephrocalcinosis = True
    obj.right_nephrolithiasis = True
    obj.right_other_malformation = 'foo'
    obj.left_present = True
    obj.left_type = 'TRANSPLANT'
    obj.left_length = 11
    obj.left_volume = 51
    obj.left_cysts = True
    obj.left_calcification = True
    obj.left_nephrocalcinosis = True
    obj.left_nephrolithiasis = True
    obj.left_other_malformation = 'bar'
    return obj


def test_valid(renal_imaging):
    obj = valid(renal_imaging)
    assert obj.date == date(2015, 1, 1)
    assert obj.imaging_type == 'USS'
    assert obj.right_present is True
    assert obj.right_type == 'NATURAL'
    assert obj.right_length == 10
    assert obj.right_volume == 50
    assert obj.right_cysts is True
    assert obj.right_calcification is True
    assert obj.right_nephrocalcinosis is True
    assert obj.right_nephrolithiasis is True
    assert obj.right_other_malformation == 'foo'
    assert obj.left_present is True
    assert obj.left_type == 'TRANSPLANT'
    assert obj.left_length == 11
    assert obj.left_volume == 51
    assert obj.left_cysts is True
    assert obj.left_calcification is True
    assert obj.left_nephrocalcinosis is True
    assert obj.left_nephrolithiasis is True
    assert obj.left_other_malformation == 'bar'
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_missing(renal_imaging):
    renal_imaging.patient = None
    invalid(renal_imaging)


def test_data_source_missing(renal_imaging):
    renal_imaging.data_source = None
    invalid(renal_imaging)


def test_date_missing(renal_imaging):
    renal_imaging.date = None
    invalid(renal_imaging)


def test_date_before_dob(renal_imaging):
    renal_imaging.date = date(1999, 1, 1)
    invalid(renal_imaging)


def test_date_in_future(renal_imaging):
    renal_imaging.date = date.today() + timedelta(days=1)
    invalid(renal_imaging)


def test_imaging_type_missing(renal_imaging):
    renal_imaging.imaging_type = None
    invalid(renal_imaging)


def test_imaging_type_blank(renal_imaging):
    renal_imaging.imaging_type = ''
    invalid(renal_imaging)


def test_imaging_type_invalid(renal_imaging):
    renal_imaging.imaging_type = 'foo'
    invalid(renal_imaging)


def test_right_present_missing(renal_imaging):
    renal_imaging.right_present = None
    invalid(renal_imaging)


def test_right_present_false(renal_imaging):
    renal_imaging.right_present = False
    obj = valid(renal_imaging)
    assert obj.right_type is None
    assert obj.right_length is None
    assert obj.right_volume is None
    assert obj.right_cysts is None
    assert obj.right_calcification is None
    assert obj.right_nephrocalcinosis is None
    assert obj.right_nephrolithiasis is None
    assert obj.right_other_malformation is None


def test_right_present_false_right_type_missing(renal_imaging):
    renal_imaging.right_present = False
    renal_imaging.right_type = None
    valid(renal_imaging)


def test_right_present_true_right_type_missing(renal_imaging):
    renal_imaging.right_present = True
    renal_imaging.right_type = None
    invalid(renal_imaging)


def test_right_present_false_right_length_missing(renal_imaging):
    renal_imaging.right_present = False
    renal_imaging.right_length = None
    valid(renal_imaging)


def test_right_present_true_right_length_missing(renal_imaging):
    renal_imaging.right_present = True
    renal_imaging.right_length = None
    valid(renal_imaging)


def test_right_present_false_right_volume_missing(renal_imaging):
    renal_imaging.right_present = False
    renal_imaging.right_volume = None
    valid(renal_imaging)


def test_right_present_true_right_volume_missing(renal_imaging):
    renal_imaging.right_present = True
    renal_imaging.right_volume = None
    valid(renal_imaging)


def test_right_present_false_right_cysts_missing(renal_imaging):
    renal_imaging.right_present = False
    renal_imaging.right_cysts = None
    valid(renal_imaging)


def test_right_present_true_right_cysts_missing(renal_imaging):
    renal_imaging.right_present = True
    renal_imaging.right_cysts = None
    invalid(renal_imaging)


def test_right_present_false_right_calcification_missing(renal_imaging):
    renal_imaging.right_present = False
    renal_imaging.right_calcification = None
    valid(renal_imaging)


def test_right_present_true_right_calcification_missing(renal_imaging):
    renal_imaging.right_present = True
    renal_imaging.right_calcification = None
    invalid(renal_imaging)


def test_right_calcification_false_right_nephrocalcinosis_missing(renal_imaging):
    renal_imaging.right_calcification = False
    renal_imaging.right_nephrocalcinosis = None
    valid(renal_imaging)


def test_right_calcification_true_right_nephrocalcinosis_missing(renal_imaging):
    renal_imaging.right_calcification = True
    renal_imaging.right_nephrocalcinosis = None
    invalid(renal_imaging)


def test_right_calcification_false_right_nephrolithiasis_missing(renal_imaging):
    renal_imaging.right_calcification = False
    renal_imaging.right_nephrolithiasis = None
    valid(renal_imaging)


def test_right_calcification_true_right_nephrolithiasis_missing(renal_imaging):
    renal_imaging.right_calcification = True
    renal_imaging.right_nephrolithiasis = None
    invalid(renal_imaging)


def test_right_other_malformation_missing(renal_imaging):
    renal_imaging.right_other_malformation = None
    valid(renal_imaging)


def test_right_other_malformation_blank(renal_imaging):
    renal_imaging.right_other_malformation = ''
    obj = valid(renal_imaging)
    assert obj.right_other_malformation is None


def test_left_present_missing(renal_imaging):
    renal_imaging.left_present = None
    invalid(renal_imaging)


def test_left_present_false(renal_imaging):
    renal_imaging.left_present = False
    obj = valid(renal_imaging)
    assert obj.left_type is None
    assert obj.left_length is None
    assert obj.left_volume is None
    assert obj.left_cysts is None
    assert obj.left_calcification is None
    assert obj.left_nephrocalcinosis is None
    assert obj.left_nephrolithiasis is None
    assert obj.left_other_malformation is None


def test_left_present_false_left_type_missing(renal_imaging):
    renal_imaging.left_present = False
    renal_imaging.left_type = None
    valid(renal_imaging)


def test_left_present_true_left_type_missing(renal_imaging):
    renal_imaging.left_present = True
    renal_imaging.left_type = None
    invalid(renal_imaging)


def test_left_present_false_left_length_missing(renal_imaging):
    renal_imaging.left_present = False
    renal_imaging.left_length = None
    valid(renal_imaging)


def test_left_present_true_left_length_missing(renal_imaging):
    renal_imaging.left_present = True
    renal_imaging.left_length = None
    valid(renal_imaging)


def test_left_present_false_left_volume_missing(renal_imaging):
    renal_imaging.left_present = False
    renal_imaging.left_volume = None
    valid(renal_imaging)


def test_left_present_true_left_volume_missing(renal_imaging):
    renal_imaging.left_present = True
    renal_imaging.left_volume = None
    valid(renal_imaging)


def test_left_present_false_left_cysts_missing(renal_imaging):
    renal_imaging.left_present = False
    renal_imaging.left_cysts = None
    valid(renal_imaging)


def test_left_present_true_left_cysts_missing(renal_imaging):
    renal_imaging.left_present = True
    renal_imaging.left_cysts = None
    invalid(renal_imaging)


def test_left_present_false_left_calcification_missing(renal_imaging):
    renal_imaging.left_present = False
    renal_imaging.left_calcification = None
    valid(renal_imaging)


def test_left_present_true_left_calcification_missing(renal_imaging):
    renal_imaging.left_present = True
    renal_imaging.left_calcification = None
    invalid(renal_imaging)


def test_left_calcification_false_left_nephrocalcinosis_missing(renal_imaging):
    renal_imaging.left_calcification = False
    renal_imaging.left_nephrocalcinosis = None
    valid(renal_imaging)


def test_left_calcification_true_left_nephrocalcinosis_missing(renal_imaging):
    renal_imaging.left_calcification = True
    renal_imaging.left_nephrocalcinosis = None
    invalid(renal_imaging)


def test_left_calcification_false_left_nephrolithiasis_missing(renal_imaging):
    renal_imaging.left_calcification = False
    renal_imaging.left_nephrolithiasis = None
    valid(renal_imaging)


def test_left_calcification_true_left_nephrolithiasis_missing(renal_imaging):
    renal_imaging.left_calcification = True
    renal_imaging.left_nephrolithiasis = None
    invalid(renal_imaging)


def test_left_other_malformation_missing(renal_imaging):
    renal_imaging.left_other_malformation = None
    valid(renal_imaging)


def test_left_other_malformation_blank(renal_imaging):
    renal_imaging.left_other_malformation = ''
    obj = valid(renal_imaging)
    assert obj.left_other_malformation is None


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(RenalImaging, RenalImagingValidation, obj, **kwargs)
