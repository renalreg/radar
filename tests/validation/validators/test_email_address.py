import pytest
from radar.lib.validation.core import ValidationError
from radar.lib.validation.validators import email_address


def test_valid():
    valid('foo@example.org')


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
    email_address()(value)


def invalid(value):
    with pytest.raises(ValidationError) as e:
        email_address()(value)

    return e
