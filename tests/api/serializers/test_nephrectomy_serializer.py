from datetime import date, timedelta

from cornflake.exceptions import ValidationError
import pytest

from radar.api.serializers.nephrectomies import NephrectomySerializer
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
def nephrectomy(patient):
    return {
        'source_group': Group(),
        'source_type': SOURCE_TYPE_MANUAL,
        'patient': patient,
        'date': date(2015, 1, 1),
        'kidney_side': 'LEFT',
        'kidney_type': 'NATIVE',
        'entry_type': 'HA'
    }


def test_valid(nephrectomy):
    obj = valid(nephrectomy)
    assert obj.date == date(2015, 1, 1)
    assert obj.kidney_side == 'LEFT'
    assert obj.kidney_type == 'NATIVE'
    assert obj.entry_type == 'HA'
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_none(nephrectomy):
    nephrectomy['patient'] = None
    invalid(nephrectomy)


def test_source_group_none(nephrectomy):
    nephrectomy['source_group'] = None
    invalid(nephrectomy)


def test_source_type_none(nephrectomy):
    nephrectomy['source_type'] = None
    nephrectomy = valid(nephrectomy)
    assert nephrectomy.source_type == SOURCE_TYPE_MANUAL


def test_date_none(nephrectomy):
    nephrectomy['date'] = None
    invalid(nephrectomy)


def test_date_before_dob(nephrectomy):
    nephrectomy['date'] = date(1999, 1, 1)
    invalid(nephrectomy)


def test_date_future(nephrectomy):
    nephrectomy['date'] = date.today() + timedelta(days=1)
    invalid(nephrectomy)


def test_kidney_side_none(nephrectomy):
    nephrectomy['kidney_side'] = None
    invalid(nephrectomy)


def test_kidney_side_invalid(nephrectomy):
    nephrectomy['kidney_side'] = 'HELLO'
    invalid(nephrectomy)


def test_kidney_type_none(nephrectomy):
    nephrectomy['kidney_type'] = None
    invalid(nephrectomy)


def test_kidney_type_invalid(nephrectomy):
    nephrectomy['kidney_type'] = 'HELLO'
    invalid(nephrectomy)


def test_entry_type_none(nephrectomy):
    nephrectomy['entry_type'] = None
    invalid(nephrectomy)


def test_entry_type_invalid(nephrectomy):
    nephrectomy['entry_type'] = 'HELLO'
    invalid(nephrectomy)


def invalid(data):
    with pytest.raises(ValidationError) as e:
        valid(data)

    return e


def valid(data):
    serializer = NephrectomySerializer(data=data, context={'user': User(is_admin=True)})
    serializer.is_valid(raise_exception=True)
    return serializer.save()
