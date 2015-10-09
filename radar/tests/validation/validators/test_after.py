from datetime import date, datetime
import pytest
import pytz
from radar.lib.validation.core import ValidationError
from radar.lib.validation.validators import after


def test_date_datetime():
    value = after(date(2015, 1, 1))(datetime(2015, 1, 1, 0, 0, 0, tzinfo=pytz.utc))
    assert value == datetime(2015, 1, 1, 0, 0, 0, tzinfo=pytz.utc)


def test_datetime_date():
    value = after(datetime(2015, 1, 1, 0, 0, 0, tzinfo=pytz.utc))(date(2015, 1, 1))
    assert value == date(2015, 1, 1)


def test_less_than():
    with pytest.raises(ValidationError):
        after(datetime(2015, 1, 1, 0, 0, 0, tzinfo=pytz.utc))(datetime(2014, 12, 31, 23, 59, 59, tzinfo=pytz.utc))


def test_equal():
    after(datetime(2015, 1, 1, 0, 0, 0, tzinfo=pytz.utc))(datetime(2015, 1, 1, 0, 0, 0, tzinfo=pytz.utc))


def test_greater_than():
    after(datetime(2015, 1, 1, 0, 0, 0, tzinfo=pytz.utc))(datetime(2015, 1, 1, 0, 0, 1, tzinfo=pytz.utc))


def test_dt_format():
    with pytest.raises(ValidationError) as e:
        after(datetime(2015, 1, 1, 0, 0, 0, tzinfo=pytz.utc), dt_format='%Y-%m-%d')(datetime(2014, 12, 31, 0, 0, 0, tzinfo=pytz.utc))

    assert e.value.errors[0] == 'Value is before 2015-01-01.'
