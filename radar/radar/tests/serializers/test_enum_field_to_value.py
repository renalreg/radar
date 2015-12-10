from enum import Enum

import pytest

from radar.serializers.fields import EnumField
from radar.validation.core import ValidationError


class Foo(Enum):
    a = 'foo'
    b = 'bar'
    c = 'baz'


def test_enum():
    assert to_value(Foo.a) is Foo.a


def test_valid_str():
    assert to_value('foo') is Foo.a


def test_invalid_str():
    to_value_invalid('hello')


def test_none():
    assert to_value(None) is None


def test_int():
    to_value_invalid(123)


def test_float():
    to_value_invalid(123.456)


def test_true():
    to_value_invalid(True)


def test_false():
    to_value_invalid(False)


def test_dict():
    to_value_invalid({'foo': 1, 'bar': 2})


def test_list():
    to_value_invalid(['foo', 'bar', 'baz'])


def to_value_invalid(data):
    with pytest.raises(ValidationError):
        to_value(data)


def to_value(data):
    field = EnumField(Foo)
    field.bind('test')
    data = field.get_data({'test': data})
    value = field.to_value(data)
    return value
