import pytest
from cornflake.exceptions import ValidationError

from radar.api.serializers.auth import ResetPasswordSerializer


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


def invalid(data):
    with pytest.raises(ValidationError) as e:
        valid(data)

    return e


def valid(data):
    serializer = ResetPasswordSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data
