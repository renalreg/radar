import pytest
from cornflake.exceptions import ValidationError

from radar.api.serializers.auth import ForgotPasswordSerializer


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


def invalid(data):
    with pytest.raises(ValidationError) as e:
        valid(data)

    return e


def valid(data):
    serializer = ForgotPasswordSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data
