import pytest
from cornflake.exceptions import ValidationError

from radar.api.serializers.auth import ForgotUsernameSerializer


def test_valid():
    obj = valid({'email': 'foo@example.org'})
    assert obj['email'] == 'foo@example.org'


def test_email_invalid():
    obj = valid({'email': 'foo'})
    assert obj['email'] == 'foo'


def test_email_missing():
    invalid({})
    invalid({'email': None})


def invalid(data):
    with pytest.raises(ValidationError) as e:
        valid(data)

    return e


def valid(data):
    serializer = ForgotUsernameSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data
