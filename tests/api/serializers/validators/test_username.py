from cornflake.exceptions import ValidationError
import pytest

from radar.api.serializers.validators import username


def test_valid():
    assert valid('alice') == 'alice'


def test_email():
    assert valid('foo@example.org') == 'foo@example.org'


def test_lower():
    assert valid('ALICE') == 'alice'


def test_dot():
    assert valid('alice.bob') == 'alice.bob'


def test_multiple_dots():
    assert valid('foo.bar.baz') == 'foo.bar.baz'


def test_number():
    assert valid('alice42') == 'alice42'


def test_lower_limit():
    assert valid('abcd') == 'abcd'


def test_upper_limit():
    assert valid('abcdefghijklymnopqrstuvwxyz12345') == 'abcdefghijklymnopqrstuvwxyz12345'


def test_underscore():
    invalid('alice_bob')


def test_dash():
    invalid('alice-bob')


def test_dot_at_start():
    invalid('.alice')


def test_dot_at_end():
    invalid('alice.')


def test_repeated_dot():
    invalid('alice...bob')


def test_too_short():
    invalid('aaa')


def test_too_long():
    invalid('abcdefghijklymnopqrstuvwxyz123456')


def valid(value):
    return username()(value)


def invalid(value):
    with pytest.raises(ValidationError) as e:
        username()(value)

    return e
