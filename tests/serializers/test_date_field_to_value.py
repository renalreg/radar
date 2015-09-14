from datetime import date, datetime

import pytest

from radar.lib.serializers import DateField
from radar.lib.validation.core import ValidationError


def test_date():
    assert to_value(date(2001, 2, 3)) == date(2001, 2, 3)


def test_date_string():
    assert to_value('2001-02-03') == date(2001, 2, 3)
    assert to_value('999-2-3') == date(999, 2, 3)


def test_datetime_string():
    assert to_value('2001-02-03T12:34:56') == date(2001, 2, 3)
    assert to_value('2001-02-03 12:34:56') == date(2001, 2, 3)


def test_none():
    assert to_value(None) is None


def test_invalid_day():
    to_value_invalid('2001-02-29')


def test_invalid_month():
    to_value_invalid('2001-13-03')


def test_datetime():
    to_value_invalid(datetime(2001, 2, 3, 12, 34, 56))


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
    field = DateField()
    field.bind('test')
    data = field.get_data({'test': data})
    value = field.to_value(data)
    return value
