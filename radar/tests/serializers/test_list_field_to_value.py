import pytest

from radar.serializers.fields import IntegerField, ListField
from radar.validation.core import ValidationError


def test_integer_list():
    assert to_value([1, 2, 3]) == [1, 2, 3]


def test_integer_string_list():
    assert to_value(['1', '2', '3']) == [1, 2, 3]


def test_none_in_list():
    assert to_value([1, None, 3]) == [1, None, 3]


def test_none_list():
    assert to_value([None]) == [None]


def test_empty_list():
    assert to_value([]) == []


def test_none():
    assert to_value(None) is None


def test_true():
    to_value_invalid(True)


def test_false():
    to_value_invalid(False)


def test_string():
    to_value_invalid('hello')


def test_int():
    to_value_invalid(123)


def test_float():
    to_value_invalid(123.456)


def test_dict():
    to_value_invalid({'foo': 1})


def test_errors():
    e = to_value_invalid([1, 'hello', 3])
    assert e.value.errors == {1: ['A valid integer is required.']}


def to_value_invalid(data):
    with pytest.raises(ValidationError) as e:
        to_value(data)

    return e


def to_value(data):
    field = ListField(IntegerField())
    field.bind('test')
    data = field.get_data({'test': data})
    value = field.to_value(data)
    return value
