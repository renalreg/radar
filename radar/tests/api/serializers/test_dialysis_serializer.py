from datetime import date, timedelta

import pytest
from cornflake.exceptions import ValidationError

from radar.api.serializers.dialysis import DialysisSerializer
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
def dialysis(patient):
    return {
        'source_group': Group(),
        'source_type': SOURCE_TYPE_RADAR,
        'patient': patient,
        'from_date': date(2015, 1, 1),
        'to_date': date(2015, 1, 2),
        'modality': 1
    }


def test_valid(dialysis):
    obj = valid(dialysis)
    assert obj.from_date == date(2015, 1, 1)
    assert obj.to_date == date(2015, 1, 2)
    assert obj.modality == 1
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_none(dialysis):
    dialysis['patient'] = None
    invalid(dialysis)


def test_source_group_none(dialysis):
    dialysis['source_group'] = None
    invalid(dialysis)


def test_source_type_none(dialysis):
    dialysis['source_type'] = None
    dialysis = valid(dialysis)
    assert dialysis.source_type == SOURCE_TYPE_RADAR


def test_source_type_missing(dialysis):
    dialysis.pop('source_type')
    dialysis = valid(dialysis)
    assert dialysis.source_type == SOURCE_TYPE_RADAR


def test_from_date_none(dialysis):
    dialysis['from_date'] = None
    invalid(dialysis)


def test_from_date_before_dob(dialysis):
    dialysis['from_date'] = date(1999, 1, 1)
    invalid(dialysis)


def test_from_date_future(dialysis):
    dialysis['from_date'] = date.today() + timedelta(days=1)
    invalid(dialysis)


def test_to_date_none(dialysis):
    dialysis['to_date'] = None
    valid(dialysis)


def test_to_date_before_dob(dialysis):
    dialysis['to_date'] = date(1999, 1, 1)
    invalid(dialysis)


def test_to_date_future(dialysis):
    dialysis['to_date'] = date.today() + timedelta(days=1)
    invalid(dialysis)


def test_to_date_before_from_date(dialysis):
    dialysis['to_date'] = dialysis['from_date'] - timedelta(days=1)
    invalid(dialysis)


def test_modality_none(dialysis):
    dialysis['modality'] = None
    invalid(dialysis)


def test_modality_invalid(dialysis):
    dialysis['modality'] = 0
    invalid(dialysis)


def invalid(data):
    with pytest.raises(ValidationError) as e:
        valid(data)

    return e


def valid(data):
    serializer = DialysisSerializer(data=data, context={'user': User(is_admin=True)})
    serializer.is_valid(raise_exception=True)
    return serializer.save()
