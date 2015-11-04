import pytest

from radar.serializers.fields import IntegerField
from radar.validation.core import ValidationError


def test_integer_string():
    assert to_value('123') == 123


def test_positive_integer_string():
    assert to_value('+123') == 123


def test_negative_integer_string():
    assert to_value('-123') == -123


def test_leading_zeros():
    assert to_value('0100') == 100


def test_whitespace():
    assert to_value('  123  ') == 123


def test_integer():
    assert to_value(123) == 123


def test_negative_integer():
    assert to_value(-123) == -123


def test_true():
    assert to_value(True) == 1


def test_false():
    assert to_value(False) == 0


def test_none():
    assert to_value(None) is None


def test_decimal():
    to_value_invalid(123.456)


def test_decimal_string():
    to_value_invalid('123.456')


def test_string():
    to_value_invalid('hello')


def test_empty_string():
    assert to_value('') is None


def test_dict():
    to_value_invalid({'foo': 1, 'bar': 2})


def test_list():
    to_value_invalid(['foo', 'bar', 'baz'])


def to_value_invalid(data):
    with pytest.raises(ValidationError):
        to_value(data)


def to_value(data):
    field = IntegerField()
    field.bind('test')
    data = field.get_data({'test': data})
    value = field.to_value(data)
    return value
