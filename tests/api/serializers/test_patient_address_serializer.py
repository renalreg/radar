from datetime import date, timedelta

import pytest
from cornflake.exceptions import ValidationError

from radar.api.serializers.patient_addresses import PatientAddressSerializer
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
def address(patient):
    return {
        'source_group': Group(),
        'source_type': SOURCE_TYPE_RADAR,
        'patient': patient,
        'from_date': date(2014, 1, 1),
        'to_date': date(2015, 1, 1),
        'address1': 'Learning and Research Building',
        'address2': 'Southmead Hospital',
        'address3': 'Bristol',
        'postcode': 'BS10 5NB',
        'country': 'UK',
    }


def test_valid(address):
    obj = valid(address)
    assert obj.from_date == date(2014, 1, 1)
    assert obj.to_date == date(2015, 1, 1)
    assert obj.address1 == 'Learning and Research Building'
    assert obj.address2 == 'Southmead Hospital'
    assert obj.address3 == 'Bristol'
    assert obj.postcode == 'BS10 5NB'
    assert obj.country == 'UK'
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_none(address):
    address['patient'] = None
    invalid(address)


def test_source_group_none(address):
    address['source_group'] = None
    invalid(address)


def test_source_type_none(address):
    address['source_type'] = None
    obj = valid(address)
    assert obj.source_type == 'RADAR'


def test_from_date_none(address):
    address['from_date'] = None
    valid(address)


def test_from_date_before_dob(address):
    address['from_date'] = date(1999, 1, 1)
    invalid(address)


def test_to_date_none(address):
    address['to_date'] = None
    valid(address)


def test_to_date_before_dob(address):
    address['from_date'] = date(1999, 1, 1)
    address['to_date'] = date(1999, 1, 2)
    invalid(address)


def test_to_date_before_from_date(address):
    address['to_date'] = address['from_date'] - timedelta(days=1)
    invalid(address)


def test_address1_blank(address):
    address['address1'] = ''
    invalid(address)


def test_address1_none(address):
    address['address1'] = None
    invalid(address)


def test_address1_comma(address):
    address['address1'] = ','
    invalid(address)


def test_address1_extra_spaces(address):
    address['address1'] = 'foo   bar'
    obj = valid(address)
    assert obj.address1 == 'foo bar'


def test_address2_blank(address):
    address['address2'] = ''
    obj = valid(address)
    assert obj.address2 is None


def test_address2_none(address):
    address['address2'] = None
    valid(address)


def test_address2_comma(address):
    address['address2'] = ','
    obj = valid(address)
    assert obj.address2 is None


def test_address2_extra_spaces(address):
    address['address2'] = 'foo   bar'
    obj = valid(address)
    assert obj.address2 == 'foo bar'


def test_address3_blank(address):
    address['address3'] = ''
    obj = valid(address)
    assert obj.address3 is None


def test_address3_none(address):
    address['address3'] = None
    valid(address)


def test_address3_comma(address):
    address['address3'] = ','
    obj = valid(address)
    assert obj.address3 is None


def test_address3_extra_spaces(address):
    address['address3'] = 'foo   bar'
    obj = valid(address)
    assert obj.address3 == 'foo bar'


def test_postcode_blank(address):
    address['postcode'] = ''
    invalid(address)


def test_postcode_none(address):
    address['postcode'] = None
    invalid(address)


def test_postcode_invalid(address):
    address['postcode'] = 'HELLO'
    invalid(address)


def invalid(data):
    with pytest.raises(ValidationError) as e:
        valid(data)

    return e


def valid(data):
    serializer = PatientAddressSerializer(data=data, context={'user': User(is_admin=True)})
    serializer.is_valid(raise_exception=True)
    return serializer.save()
