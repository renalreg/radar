from cornflake.exceptions import ValidationError
import pytest

from radar.api.serializers.patient_numbers import PatientNumberSerializer
from radar.models.groups import (
    Group,
    GROUP_CODE_CHI,
    GROUP_CODE_HSC,
    GROUP_CODE_NHS,
    GROUP_CODE_RADAR,
    GROUP_CODE_UKRR,
    GROUP_TYPE,
)
from radar.models.patients import Patient
from radar.models.source_types import SOURCE_TYPE_MANUAL
from radar.models.users import User


@pytest.fixture
def patient():
    patient = Patient()
    return patient


@pytest.fixture
def number(patient):
    return {
        'source_group': Group(),
        'source_type': SOURCE_TYPE_MANUAL,
        'patient': patient,
        'number_group': Group(code='FOO', type=GROUP_TYPE.OTHER),
        'number': '123'
    }


def test_valid(number):
    number_group = number['number_group']
    obj = valid(number)
    assert obj.number_group == number_group
    assert obj.number == '123'
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_none(number):
    number['patient'] = None
    invalid(number)


def test_source_group_none(number):
    number['source_group'] = None
    invalid(number)


def test_source_type_none(number):
    number['source_type'] = None
    number = valid(number)
    assert number.source_type == SOURCE_TYPE_MANUAL


def test_number_group_none(number):
    number['number_group'] = None
    invalid(number)


def test_number_group_radar(number):
    number['number_group'] = Group(code=GROUP_CODE_RADAR, type=GROUP_TYPE.SYSTEM)
    invalid(number)


def test_number_none(number):
    number['number'] = None
    invalid(number)


def test_number_blank(number):
    number['number'] = ''
    invalid(number)


def test_number_remove_extra_spaces(number):
    number['number'] = '123   456'
    obj = valid(number)
    assert obj.number == '123 456'


def test_nhs_no_valid(number):
    number['number_group'] = Group(code=GROUP_CODE_NHS, type=GROUP_TYPE.OTHER)
    number['number'] = '9434765919'
    valid(number)


def test_nhs_no_invalid(number):
    number['number_group'] = Group(code=GROUP_CODE_NHS, type=GROUP_TYPE.OTHER)
    number['number'] = '9434765918'
    invalid(number)


def test_chi_no_valid(number):
    number['number_group'] = Group(code=GROUP_CODE_CHI, type=GROUP_TYPE.OTHER)
    number['number'] = '101299877'
    valid(number)


def test_chi_no_invalid(number):
    number['number_group'] = Group(code=GROUP_CODE_CHI, type=GROUP_TYPE.OTHER)
    number['number'] = '9434765918'
    invalid(number)


def test_hsc_no_valid(number):
    number['number_group'] = Group(code=GROUP_CODE_HSC, type=GROUP_TYPE.OTHER)
    number['number'] = '3232255825'
    valid(number)


def test_hsc_no_invalid(number):
    number['number_group'] = Group(code=GROUP_CODE_HSC, type=GROUP_TYPE.OTHER)
    number['number'] = '9434765918'
    invalid(number)


def test_ukrr_no_valid(number):
    number['number_group'] = Group(code=GROUP_CODE_UKRR, type=GROUP_TYPE.OTHER)
    number['number'] = '200012345'
    valid(number)


def test_ukrr_no_invalid(number):
    number['number_group'] = Group(code=GROUP_CODE_UKRR, type=GROUP_TYPE.OTHER)
    number['number'] = '2000123456'
    invalid(number)


def invalid(data):
    with pytest.raises(ValidationError) as e:
        valid(data)

    return e


def valid(data):
    serializer = PatientNumberSerializer(data=data, context={'user': User(is_admin=True)})
    serializer.is_valid(raise_exception=True)
    return serializer.save()
