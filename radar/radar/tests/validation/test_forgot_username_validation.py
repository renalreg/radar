import pytest

from radar.validation.forgot_username import ForgotUsernameValidation
from radar.validation.core import ValidationError
from radar.tests.helpers.validation import validation_runner


def test_valid():
    obj = valid({'email': 'foo@example.org'})
    assert obj['email'] == 'foo@example.org'


def test_email_invalid():
    obj = valid({'email': 'foo'})
    assert obj['email'] == 'foo'


def test_email_missing():
    invalid({})
    invalid({'email': None})


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(dict, ForgotUsernameValidation, obj, **kwargs)
