from datetime import datetime, date
import pytest
import pytz
from radar.lib.serializers import DateTimeField
from radar.lib.validation.core import ValidationError


def test_string():
    assert to_value('2001-02-03 12:34:56') == datetime(2001, 2, 3, 12, 34, 56, tzinfo=pytz.UTC)


def test_t_string():
    assert to_value('2001-02-03T12:34:56') == datetime(2001, 2, 3, 12, 34, 56, tzinfo=pytz.UTC)


def test_negative_offset_string():
    assert to_value('2001-02-03T12:34:56-01:00') == datetime(2001, 2, 3, 13, 34, 56, tzinfo=pytz.UTC)


def test_positive_offset_string():
    assert to_value('2001-02-03T12:34:56+01:00') == datetime(2001, 2, 3, 11, 34, 56, tzinfo=pytz.UTC)


def test_date_string():
    assert to_value('2001-02-03') == datetime(2001, 2, 3, 0, 0, 0, tzinfo=pytz.UTC)


def test_none():
    assert to_value(None) is None


def test_datetime():
    assert to_value(datetime(2001, 2, 3, 12, 34, 56)) == datetime(2001, 2, 3, 12, 34, 56)


def test_invalid_month_string():
    to_value_invalid('2001-13-03T12:34:56')


def test_invalid_day_string():
    to_value_invalid('2001-02-29T12:34:56')


def test_invalid_hour_string():
    to_value_invalid('2001-02-03T24:34:56')


def test_invalid_minute_string():
    to_value_invalid('2001-02-03T12:60:56')


def test_invalid_second_string():
    to_value_invalid('2001-02-03T12:34:60')


def test_date():
    to_value_invalid(date(2001, 2, 3))


def test_int():
    to_value_invalid(2000)


def test_float():
    to_value_invalid(2000.1)


def test_true():
    to_value_invalid(True)


def test_false():
    to_value_invalid(False)


def test_invalid_string():
    to_value_invalid('hello')


def test_dict():
    to_value_invalid({'foo': 1})


def test_list():
    to_value_invalid(['foo'])


def to_value_invalid(data):
    with pytest.raises(ValidationError):
        to_value(data)


def to_value(data):
    field = DateTimeField()
    field.bind('test')
    data = field.get_data({'test': data})
    value = field.to_value(data)
    return value
