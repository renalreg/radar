from datetime import date, timedelta

from cornflake.exceptions import ValidationError
import pytest

from radar.api.serializers.renal_imaging import RenalImagingSerializer
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
def renal_imaging(patient):
    return {
        'source_group': Group(),
        'source_type': SOURCE_TYPE_MANUAL,
        'patient': patient,
        'date': date(2015, 1, 1),
        'imaging_type': 'USS',
        'right_present': True,
        'right_type': 'NATIVE',
        'right_length': 10,
        'right_volume': 50,
        'right_cysts': True,
        'right_stones': True,
        'right_calcification': True,
        'right_nephrocalcinosis': True,
        'right_nephrolithiasis': True,
        'right_other_malformation': 'foo',
        'left_present': True,
        'left_type': 'TRANSPLANT',
        'left_length': 11,
        'left_volume': 51,
        'left_cysts': True,
        'left_stones': True,
        'left_calcification': True,
        'left_nephrocalcinosis': True,
        'left_nephrolithiasis': True,
        'left_other_malformation': 'bar'
    }


def test_valid(renal_imaging):
    obj = valid(renal_imaging)
    assert obj.date == date(2015, 1, 1)
    assert obj.imaging_type == 'USS'
    assert obj.right_present is True
    assert obj.right_type == 'NATIVE'
    assert obj.right_length == 10
    assert obj.right_volume == 50
    assert obj.right_cysts is True
    assert obj.right_stones is True
    assert obj.right_calcification is True
    assert obj.right_nephrocalcinosis is True
    assert obj.right_nephrolithiasis is True
    assert obj.right_other_malformation == 'foo'
    assert obj.left_present is True
    assert obj.left_type == 'TRANSPLANT'
    assert obj.left_length == 11
    assert obj.left_volume == 51
    assert obj.left_cysts is True
    assert obj.left_stones is True
    assert obj.left_calcification is True
    assert obj.left_nephrocalcinosis is True
    assert obj.left_nephrolithiasis is True
    assert obj.left_other_malformation == 'bar'
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_none(renal_imaging):
    renal_imaging['patient'] = None
    invalid(renal_imaging)


def test_source_group_none(renal_imaging):
    renal_imaging['source_group'] = None
    invalid(renal_imaging)


def test_source_type_none(renal_imaging):
    renal_imaging['source_type'] = None
    obj = valid(renal_imaging)
    assert obj.source_type == SOURCE_TYPE_MANUAL


def test_date_none(renal_imaging):
    renal_imaging['date'] = None
    invalid(renal_imaging)


def test_date_before_dob(renal_imaging):
    renal_imaging['date'] = date(1999, 1, 1)
    invalid(renal_imaging)


def test_date_in_future(renal_imaging):
    renal_imaging['date'] = date.today() + timedelta(days=1)
    invalid(renal_imaging)


def test_imaging_type_none(renal_imaging):
    renal_imaging['imaging_type'] = None
    invalid(renal_imaging)


def test_imaging_type_blank(renal_imaging):
    renal_imaging['imaging_type'] = ''
    invalid(renal_imaging)


def test_imaging_type_invalid(renal_imaging):
    renal_imaging['imaging_type'] = 'foo'
    invalid(renal_imaging)


def test_right_present_none(renal_imaging):
    renal_imaging['right_present'] = None
    valid(renal_imaging)


def test_right_present_false(renal_imaging):
    renal_imaging['right_present'] = False
    obj = valid(renal_imaging)
    assert obj.right_type is None
    assert obj.right_length is None
    assert obj.right_volume is None
    assert obj.right_cysts is None
    assert obj.right_calcification is None
    assert obj.right_nephrocalcinosis is None
    assert obj.right_nephrolithiasis is None
    assert obj.right_other_malformation is None


def test_right_present_false_right_type_none(renal_imaging):
    renal_imaging['right_present'] = False
    renal_imaging['right_type'] = None
    valid(renal_imaging)


def test_right_present_true_right_type_none(renal_imaging):
    renal_imaging['right_present'] = True
    renal_imaging['right_type'] = None
    invalid(renal_imaging)


def test_right_present_false_right_length_none(renal_imaging):
    renal_imaging['right_present'] = False
    renal_imaging['right_length'] = None
    valid(renal_imaging)


def test_right_present_true_right_length_none(renal_imaging):
    renal_imaging['right_present'] = True
    renal_imaging['right_length'] = None
    valid(renal_imaging)


def test_right_present_false_right_volume_none(renal_imaging):
    renal_imaging['right_present'] = False
    renal_imaging['right_volume'] = None
    valid(renal_imaging)


def test_right_present_true_right_volume_none(renal_imaging):
    renal_imaging['right_present'] = True
    renal_imaging['right_volume'] = None
    valid(renal_imaging)


def test_right_present_false_right_cysts_none(renal_imaging):
    renal_imaging['right_present'] = False
    renal_imaging['right_cysts'] = None
    valid(renal_imaging)


def test_right_present_true_right_cysts_none(renal_imaging):
    renal_imaging['right_present'] = True
    renal_imaging['right_cysts'] = None
    invalid(renal_imaging)


def test_right_present_false_right_calcification_none(renal_imaging):
    renal_imaging['right_present'] = False
    renal_imaging['right_calcification'] = None
    valid(renal_imaging)


def test_right_present_true_right_calcification_none(renal_imaging):
    renal_imaging['right_present'] = True
    renal_imaging['right_calcification'] = None
    invalid(renal_imaging)


def test_right_calcification_false_right_nephrocalcinosis_none(renal_imaging):
    renal_imaging['right_calcification'] = False
    renal_imaging['right_nephrocalcinosis'] = None
    valid(renal_imaging)


def test_right_calcification_true_right_nephrocalcinosis_none(renal_imaging):
    renal_imaging['right_calcification'] = True
    renal_imaging['right_nephrocalcinosis'] = None
    invalid(renal_imaging)


def test_right_calcification_false_right_nephrolithiasis_none(renal_imaging):
    renal_imaging['right_calcification'] = False
    renal_imaging['right_nephrolithiasis'] = None
    valid(renal_imaging)


def test_right_calcification_true_right_nephrolithiasis_none(renal_imaging):
    renal_imaging['right_calcification'] = True
    renal_imaging['right_nephrolithiasis'] = None
    invalid(renal_imaging)


def test_right_other_malformation_none(renal_imaging):
    renal_imaging['right_other_malformation'] = None
    valid(renal_imaging)


def test_right_other_malformation_blank(renal_imaging):
    renal_imaging['right_other_malformation'] = ''
    obj = valid(renal_imaging)
    assert obj.right_other_malformation is None


def test_left_present_none(renal_imaging):
    renal_imaging['left_present'] = None
    valid(renal_imaging)


def test_left_present_false(renal_imaging):
    renal_imaging['left_present'] = False
    obj = valid(renal_imaging)
    assert obj.left_type is None
    assert obj.left_length is None
    assert obj.left_volume is None
    assert obj.left_cysts is None
    assert obj.left_calcification is None
    assert obj.left_nephrocalcinosis is None
    assert obj.left_nephrolithiasis is None
    assert obj.left_other_malformation is None


def test_left_present_false_left_type_none(renal_imaging):
    renal_imaging['left_present'] = False
    renal_imaging['left_type'] = None
    valid(renal_imaging)


def test_left_present_true_left_type_none(renal_imaging):
    renal_imaging['left_present'] = True
    renal_imaging['left_type'] = None
    invalid(renal_imaging)


def test_left_present_false_left_length_none(renal_imaging):
    renal_imaging['left_present'] = False
    renal_imaging['left_length'] = None
    valid(renal_imaging)


def test_left_present_true_left_length_none(renal_imaging):
    renal_imaging['left_present'] = True
    renal_imaging['left_length'] = None
    valid(renal_imaging)


def test_left_present_false_left_volume_none(renal_imaging):
    renal_imaging['left_present'] = False
    renal_imaging['left_volume'] = None
    valid(renal_imaging)


def test_left_present_true_left_volume_none(renal_imaging):
    renal_imaging['left_present'] = True
    renal_imaging['left_volume'] = None
    valid(renal_imaging)


def test_left_present_false_left_cysts_none(renal_imaging):
    renal_imaging['left_present'] = False
    renal_imaging['left_cysts'] = None
    valid(renal_imaging)


def test_left_present_true_left_cysts_none(renal_imaging):
    renal_imaging['left_present'] = True
    renal_imaging['left_cysts'] = None
    invalid(renal_imaging)


def test_left_present_false_left_calcification_none(renal_imaging):
    renal_imaging['left_present'] = False
    renal_imaging['left_calcification'] = None
    valid(renal_imaging)


def test_left_present_true_left_calcification_none(renal_imaging):
    renal_imaging['left_present'] = True
    renal_imaging['left_calcification'] = None
    invalid(renal_imaging)


def test_left_calcification_false_left_nephrocalcinosis_none(renal_imaging):
    renal_imaging['left_calcification'] = False
    renal_imaging['left_nephrocalcinosis'] = None
    valid(renal_imaging)


def test_left_calcification_true_left_nephrocalcinosis_none(renal_imaging):
    renal_imaging['left_calcification'] = True
    renal_imaging['left_nephrocalcinosis'] = None
    invalid(renal_imaging)


def test_left_calcification_false_left_nephrolithiasis_none(renal_imaging):
    renal_imaging['left_calcification'] = False
    renal_imaging['left_nephrolithiasis'] = None
    valid(renal_imaging)


def test_left_calcification_true_left_nephrolithiasis_none(renal_imaging):
    renal_imaging['left_calcification'] = True
    renal_imaging['left_nephrolithiasis'] = None
    invalid(renal_imaging)


def test_left_other_malformation_none(renal_imaging):
    renal_imaging['left_other_malformation'] = None
    valid(renal_imaging)


def test_left_other_malformation_blank(renal_imaging):
    renal_imaging['left_other_malformation'] = ''
    obj = valid(renal_imaging)
    assert obj.left_other_malformation is None


def test_present_none(renal_imaging):
    renal_imaging['right_present'] = None
    renal_imaging['left_present'] = None
    invalid(renal_imaging)


def invalid(data):
    with pytest.raises(ValidationError) as e:
        valid(data)

    return e


def valid(data):
    serializer = RenalImagingSerializer(data=data, context={'user': User(is_admin=True)})
    serializer.is_valid(raise_exception=True)
    return serializer.save()
