import pytest
from radar.validation.core import ValidationError
from radar.validation.validators import password


def test_xkcd():
    valid('correcthorsestaplebattery')


def test_lower_limit():
    valid('0Tvy0ugJ')


def test_too_short():
    invalid('0Tvy0ug')


def valid(value):
    new_value = password()(value)
    assert new_value == value
    return new_value


def invalid(value):
    with pytest.raises(ValidationError) as e:
        password()(value)

    return e
