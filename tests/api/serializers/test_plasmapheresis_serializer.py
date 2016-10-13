from datetime import date, timedelta

import pytest
from cornflake.exceptions import ValidationError

from radar.api.serializers.plasmapheresis import PlasmapheresisSerializer
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
def plasmapheresis(patient):
    return {
        'source_group': Group(),
        'source_type': SOURCE_TYPE_MANUAL,
        'patient': patient,
        'from_date': date(2015, 1, 1),
        'to_date': date(2015, 1, 2),
        'no_of_exchanges': '1/1D',
        'response': 'COMPLETE'
    }


def test_valid(plasmapheresis):
    obj = valid(plasmapheresis)
    assert obj.from_date == date(2015, 1, 1)
    assert obj.to_date == date(2015, 1, 2)
    assert obj.no_of_exchanges == '1/1D'
    assert obj.response == 'COMPLETE'
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_none(plasmapheresis):
    plasmapheresis['patient'] = None
    invalid(plasmapheresis)


def test_source_group_none(plasmapheresis):
    plasmapheresis['source_group'] = None
    invalid(plasmapheresis)


def test_source_type_none(plasmapheresis):
    plasmapheresis['source_type'] = None
    obj = valid(plasmapheresis)
    assert obj.source_type == SOURCE_TYPE_MANUAL


def test_from_date_none(plasmapheresis):
    plasmapheresis['from_date'] = None
    invalid(plasmapheresis)


def test_from_date_before_dob(plasmapheresis):
    plasmapheresis['from_date'] = date(1999, 1, 1)
    invalid(plasmapheresis)


def test_from_date_future(plasmapheresis):
    plasmapheresis['from_date'] = date.today() + timedelta(days=1)
    invalid(plasmapheresis)


def test_to_date_none(plasmapheresis):
    plasmapheresis['to_date'] = None
    valid(plasmapheresis)


def test_to_date_before_dob(plasmapheresis):
    plasmapheresis['to_date'] = date(1999, 1, 1)
    invalid(plasmapheresis)


def test_to_date_future(plasmapheresis):
    plasmapheresis['to_date'] = date.today() + timedelta(days=1)
    invalid(plasmapheresis)


def test_to_date_before_from_date(plasmapheresis):
    plasmapheresis['to_date'] = plasmapheresis['from_date'] - timedelta(days=1)
    invalid(plasmapheresis)


def test_no_of_exchanges_none(plasmapheresis):
    plasmapheresis['no_of_exchanges'] = None
    valid(plasmapheresis)


def test_no_of_exchanges_invalid(plasmapheresis):
    plasmapheresis['no_of_exchanges'] = 'FOO'
    invalid(plasmapheresis)


def test_response_none(plasmapheresis):
    plasmapheresis['response'] = None
    valid(plasmapheresis)


def test_response_invalid(plasmapheresis):
    plasmapheresis['response'] = 'FOO'
    invalid(plasmapheresis)


def invalid(data):
    with pytest.raises(ValidationError) as e:
        valid(data)

    return e


def valid(data):
    serializer = PlasmapheresisSerializer(data=data, context={'user': User(is_admin=True)})
    serializer.is_valid(raise_exception=True)
    return serializer.save()
