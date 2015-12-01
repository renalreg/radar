import pytest

from radar.validation.reset_password import ResetPasswordValidation
from radar.validation.core import ValidationError
from radar.tests.validation.helpers import validation_runner


def test_valid(app):
    with app.app_context():
        obj = valid({
            'token': '12345',
            'username': 'hello',
            'password': '2irPtfNUURf8G',
        })
        assert obj['token'] == '12345'
        assert obj['username'] == 'hello'
        assert obj['password'] == '2irPtfNUURf8G'


def test_token_missing(app):
    with app.app_context():
        invalid({
            'username': 'hello',
            'password': 'password',
        })


def test_username_missing(app):
    with app.app_context():
        invalid({
            'token': '12345',
            'password': 'password',
        })


def test_password_missing(app):
    with app.app_context():
        invalid({
            'token': '12345',
            'username': 'hello',
        })


def test_weak_password(app):
    with app.app_context():
        invalid({
            'token': '12345',
            'username': 'hello',
            'password': 'password',
        })


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(dict, ResetPasswordValidation, obj, **kwargs)
