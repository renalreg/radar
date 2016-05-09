import pytest

from radar.validation.core import ValidationError
from radar.validation.validators import min_crack_time


TEST_MIN_CRACK_TIME = 10E9


def test_weak():
    invalid('password')


def test_strong():
    valid('cSY6EkyYjXbmwU8ksr8DPicPqKZ8YFd7HdXs+eEiW0Q=')


def valid(value):
    return min_crack_time(TEST_MIN_CRACK_TIME)(value)


def invalid(value):
    with pytest.raises(ValidationError) as e:
        min_crack_time(TEST_MIN_CRACK_TIME)(value)

    return e
