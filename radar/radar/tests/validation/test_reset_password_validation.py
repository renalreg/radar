import pytest

from radar.validation.reset_password import ResetPasswordValidation
from radar.validation.core import ValidationError
from radar.tests.helpers.validation import validation_runner


def test_valid():
    obj = valid({
        'token': '12345',
        'username': 'hello',
        'password': 'password',
    })
    assert obj['token'] == '12345'
    assert obj['username'] == 'hello'
    assert obj['password'] == 'password'


def test_token_missing():
    invalid({
        'username': 'hello',
        'password': 'password',
    })


def test_username_missing():
    invalid({
        'token': '12345',
        'password': 'password',
    })


def test_password_missing():
    invalid({
        'token': '12345',
        'username': 'hello',
    })


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(dict, ResetPasswordValidation, obj, **kwargs)
