import pytest
from radar.lib.validation.core import ValidationError
from test_serializer import FooSerializer


def test_dict():
    assert to_value({'foo': '1', 'bar': '2'}) == {'foo': 1, 'bar': 2}


def test_dict_none():
    assert to_value({'foo': None, 'bar': '2'}) == {'foo': None, 'bar': 2}


def test_dict_missing():
    assert to_value({'bar': '2'}) == {'bar': 2}


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


def test_list():
    to_value_invalid(['foo', 'bar', 'baz'])


def to_value_invalid(data):
    with pytest.raises(ValidationError):
        to_value(data)


def to_value(data):
    field = FooSerializer()
    field.bind('test')
    data = field.get_data({'test': data})
    value = field.to_value(data)
    return value
