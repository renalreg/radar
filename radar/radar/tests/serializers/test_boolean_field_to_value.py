import pytest

from radar.serializers.fields import BooleanField
from radar.validation.core import ValidationError


def test_true():
    assert to_value(True) is True


def test_false():
    assert to_value(False) is False


def test_1():
    assert to_value(1) is True


def test_0():
    assert to_value(0) is False


def test_t_string():
    assert to_value('t') is True
    assert to_value('T') is True


def test_f_string():
    assert to_value('f') is False
    assert to_value('F') is False


def test_true_string():
    assert to_value('true') is True
    assert to_value('True') is True
    assert to_value('TRUE') is True


def test_false_string():
    assert to_value('false') is False
    assert to_value('False') is False
    assert to_value('FALSE') is False


def test_y_string():
    assert to_value('y') is True
    assert to_value('Y') is True


def test_n_string():
    assert to_value('n') is False
    assert to_value('N') is False


def test_yes_string():
    assert to_value('yes') is True
    assert to_value('Yes') is True
    assert to_value('YES') is True


def test_no_string():
    assert to_value('no') is False
    assert to_value('No') is False
    assert to_value('NO') is False


def test_1_string():
    assert to_value('1') is True


def test_0_string():
    assert to_value('0') is False


def test_none():
    assert to_value(None) is None


def test_decimal():
    to_value_invalid(123.456)


def test_decimal_string():
    to_value_invalid('1.0')


def test_dict():
    to_value_invalid({'foo': 1, 'bar': 2})


def test_list():
    to_value_invalid(['foo', 'bar', 'baz'])


def to_value_invalid(data):
    with pytest.raises(ValidationError):
        to_value(data)


def to_value(data):
    field = BooleanField()
    field.bind('test')
    data = field.get_data({'test': data})
    value = field.to_value(data)
    return value
