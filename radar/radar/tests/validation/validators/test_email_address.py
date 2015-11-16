import pytest

from radar.validation.core import ValidationError
from radar.validation.validators import email_address


def test_valid():
    assert valid('foo@example.org') == 'foo@example.org'
    assert valid('a@a.a') == 'a@a.a'


def test_upper():
    # Email addresses should be treated as case-insensitive (despite RFC 5321)
    assert valid('FOO@EXAMPLE.ORG') == 'foo@example.org'


def test_no_dot():
    invalid('foo@localhost')


def test_dot_at_start():
    invalid('foo@.example.org')


def test_dot_at_end():
    invalid('foo@example.org.')


def test_no_host():
    invalid('foo@')


def test_no_at():
    invalid('foo')


def test_no_user():
    invalid('@example.org')


def valid(value):
    return email_address()(value)


def invalid(value):
    with pytest.raises(ValidationError) as e:
        email_address()(value)

    return e
