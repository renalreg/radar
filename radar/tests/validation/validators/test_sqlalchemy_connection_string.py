import pytest

from radar.validation.core import ValidationError
from radar.validation.validators import sqlalchemy_connection_string


def test_invalid():
    invalid('not even close')


def test_valid():
    valid('postgres:///radar')


def valid(value):
    return sqlalchemy_connection_string()(value)


def invalid(value):
    with pytest.raises(ValidationError) as e:
        sqlalchemy_connection_string()(value)

    return e
