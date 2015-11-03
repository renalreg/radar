import pytest

from radar.validation.forgot_password import ForgotPasswordValidation
from radar.validation.core import ValidationError
from helpers.validation import validation_runner


def test_valid():
    obj = valid({'username': 'foo'})
    assert obj['username'] == 'foo'


def test_username_missing():
    invalid({})
    invalid({'username': None})


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(dict, ForgotPasswordValidation, obj, **kwargs)
