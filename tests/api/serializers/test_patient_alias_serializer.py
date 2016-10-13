from datetime import date

from cornflake.exceptions import ValidationError
import pytest

from radar.api.serializers.patient_aliases import PatientAliasSerializer
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
def alias(patient):
    return {
        'source_group': Group(),
        'source_type': SOURCE_TYPE_MANUAL,
        'patient': patient,
        'first_name': 'JOHN',
        'last_name': 'SMITH'
    }


def test_valid(alias):
    obj = valid(alias)
    assert obj.first_name == 'JOHN'
    assert obj.last_name == 'SMITH'
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_none(alias):
    alias['patient'] = None
    invalid(alias)


def test_source_group_none(alias):
    alias['source_group'] = None
    invalid(alias)


def test_source_type_none(alias):
    alias['source_type'] = None
    obj = valid(alias)
    assert obj.source_type == SOURCE_TYPE_MANUAL


def test_first_name_blank(alias):
    alias['first_name'] = ''
    invalid(alias)


def test_first_name_none(alias):
    alias['first_name'] = None
    invalid(alias)


def test_first_name_whitespace(alias):
    alias['first_name'] = 'FOO  BAR'
    obj = valid(alias)
    assert obj.first_name == 'FOO BAR'


def test_first_name_to_upper(alias):
    alias['first_name'] = 'foo bar'
    obj = valid(alias)
    assert obj.first_name == 'FOO BAR'


def test_last_name_blank(alias):
    alias['last_name'] = ''
    invalid(alias)


def test_last_name_none(alias):
    alias['last_name'] = None
    invalid(alias)


def test_last_name_whitespace(alias):
    alias['last_name'] = 'FOO  BAR'
    obj = valid(alias)
    assert obj.last_name == 'FOO BAR'


def test_last_name_to_upper(alias):
    alias['last_name'] = 'foo bar'
    obj = valid(alias)
    assert obj.last_name == 'FOO BAR'


def invalid(data):
    with pytest.raises(ValidationError) as e:
        valid(data)

    return e


def valid(data):
    serializer = PatientAliasSerializer(data=data, context={'user': User(is_admin=True)})
    serializer.is_valid(raise_exception=True)
    return serializer.save()
