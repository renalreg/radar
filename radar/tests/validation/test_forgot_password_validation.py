import pytest

from radar.validation.forgot_password import ForgotPasswordValidation
from radar.validation.core import ValidationError
from radar.tests.validation.helpers import validation_runner


def test_valid():
    obj = valid({'username': 'foo', 'email': 'foo@example.org'})
    assert obj['username'] == 'foo'
    assert obj['email'] == 'foo@example.org'


def test_username_missing():
    invalid({})
    invalid({'username': None})


def test_email_missing():
    invalid({})
    invalid({'email': None})


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(dict, ForgotPasswordValidation, obj, **kwargs)
