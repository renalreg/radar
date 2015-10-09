from decimal import Decimal

import pytest

from radar.lib.serializers.fields import FloatField
from radar.lib.validation.core import ValidationError


def test_float():
    assert to_value(123.456) == 123.456


def test_negative_float():
    assert to_value(-123.456) == -123.456


def test_float_string():
    assert to_value('123.456') == 123.456


def test_positive_float_string():
    assert to_value('+123.456') == 123.456


def test_negative_float_string():
    assert to_value('-123.456') == -123.456


def test_whitespace():
    assert to_value(' 123.456 ') == 123.456


def test_int():
    assert to_value(123) == 123


def test_decimal():
    assert to_value(Decimal('123.456')) == 123.456


def test_true():
    assert to_value(True) == 1


def test_false():
    assert to_value(False) == 0


def test_none():
    assert to_value(None) is None


def test_dict():
    to_value_invalid({'foo': 1, 'bar': 2})


def test_list():
    to_value_invalid(['foo', 'bar', 'baz'])


def to_value_invalid(data):
    with pytest.raises(ValidationError):
        to_value(data)


def to_value(data):
    field = FloatField()
    field.bind('test')
    data = field.get_data({'test': data})
    value = field.to_value(data)
    return value
