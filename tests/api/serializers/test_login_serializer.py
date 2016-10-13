from cornflake.exceptions import ValidationError
import pytest

from radar.api.serializers.auth import LoginSerializer


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


def invalid(data):
    with pytest.raises(ValidationError) as e:
        valid(data)

    return e


def valid(data):
    serializer = LoginSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data
