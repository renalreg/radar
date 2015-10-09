from datetime import date, datetime
import pytest
import pytz
from radar.validation.core import ValidationError
from radar.validation.validators import before


def test_date_datetime():
    value = before(date(2015, 1, 1))(datetime(2014, 12, 31, 23, 59, 59, tzinfo=pytz.utc))
    assert value == datetime(2014, 12, 31, 23, 59, 59, tzinfo=pytz.utc)


def test_datetime_date():
    value = before(datetime(2015, 1, 1, 0, 0, 0, tzinfo=pytz.utc))(date(2014, 12, 31))
    assert value == date(2014, 12, 31)


def test_less_than():
    before(datetime(2015, 1, 1, 0, 0, 0, tzinfo=pytz.utc))(datetime(2014, 12, 31, 23, 59, 59, tzinfo=pytz.utc))


def test_equal():
    before(datetime(2015, 1, 1, 0, 0, 0, tzinfo=pytz.utc))(datetime(2015, 1, 1, 0, 0, 0, tzinfo=pytz.utc))


def test_greater_than():
    with pytest.raises(ValidationError):
        before(datetime(2015, 1, 1, 0, 0, 0, tzinfo=pytz.utc))(datetime(2015, 1, 1, 0, 0, 1, tzinfo=pytz.utc))


def test_dt_format():
    with pytest.raises(ValidationError) as e:
        before(datetime(2015, 1, 1, 0, 0, 0, tzinfo=pytz.utc), dt_format='%Y-%m-%d')(datetime(2015, 1, 2, 0, 0, 0, tzinfo=pytz.utc))

    assert e.value.errors[0] == 'Value is after 2015-01-01.'
