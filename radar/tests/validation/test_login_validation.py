import pytest

from radar.validation.login import LoginValidation
from radar.validation.core import ValidationError
from utils import validation_runner


def test_valid():
    obj = valid({
        'username': 'foo',
        'password': 'bar',
        'logout_other_sessions': False,
    })
    assert obj['username'] == 'foo'
    assert obj['password'] == 'bar'
    assert obj['logout_other_sessions'] is False


def test_username_missing():
    invalid({
        'password': 'bar',
        'logout_other_sessions': False,
    })


def test_password_missing():
    invalid({
        'username': 'foo',
        'logout_other_sessions': False,
    })


def test_logout_other_sessions_missing():
    valid({
        'username': 'foo',
        'password': 'bar',
    })


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(dict, LoginValidation, obj, **kwargs)
