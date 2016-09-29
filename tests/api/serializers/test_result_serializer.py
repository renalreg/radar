from datetime import date, datetime

import pytest
from cornflake.exceptions import ValidationError
import pytz

from radar.api.serializers.results import ResultSerializer
from radar.models.groups import Group
from radar.models.patient_demographics import PatientDemographics
from radar.models.patients import Patient
from radar.models.source_types import SOURCE_TYPE_RADAR
from radar.models.users import User
from radar.models.results import Observation, OBSERVATION_VALUE_TYPE


def make(observation, value):
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)

    return {
        'source_group': Group(),
        'source_type': SOURCE_TYPE_RADAR,
        'patient': patient,
        'observation': observation,
        'date': datetime(2016, 1, 1, tzinfo=pytz.UTC),
        'value': value
    }


@pytest.mark.parametrize('value_type', [OBSERVATION_VALUE_TYPE.INTEGER, OBSERVATION_VALUE_TYPE.REAL])
def test_min_value(value_type):
    observation = Observation()
    observation.value_type = value_type
    observation.min_value = 2

    assert invalid(make(observation, 1))
    assert valid(make(observation, 2))
    assert valid(make(observation, 3))


@pytest.mark.parametrize('value_type', [OBSERVATION_VALUE_TYPE.INTEGER, OBSERVATION_VALUE_TYPE.REAL])
def test_max_value(value_type):
    observation = Observation()
    observation.value_type = value_type
    observation.properties = {}
    observation.max_value = 2

    assert valid(make(observation, 1))
    assert valid(make(observation, 2))
    assert invalid(make(observation, 3))


def test_min_length():
    observation = Observation()
    observation.value_type = OBSERVATION_VALUE_TYPE.STRING
    observation.properties = {}
    observation.min_length = 2

    assert invalid(make(observation, 'a'))
    assert valid(make(observation, 'aa'))
    assert valid(make(observation, 'aaa'))


def test_max_length():
    observation = Observation()
    observation.value_type = OBSERVATION_VALUE_TYPE.STRING
    observation.properties = {}
    observation.max_length = 2

    assert valid(make(observation, 'a'))
    assert valid(make(observation, 'aa'))
    assert invalid(make(observation, 'aaa'))


def test_options():
    observation = Observation()
    observation.value_type = OBSERVATION_VALUE_TYPE.ENUM
    observation.properties = {}
    observation.options_dict = {
        '1': 'A',
        '2': 'B',
    }

    assert valid(make(observation, '1'))
    assert valid(make(observation, '2'))
    assert invalid(make(observation, '3'))


def invalid(data):
    with pytest.raises(ValidationError) as e:
        valid(data)

    return e


def valid(data):
    serializer = ResultSerializer(context={'user': User(is_admin=True)})
    validated_data = serializer.run_validation(data)
    return validated_data
