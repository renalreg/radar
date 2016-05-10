from datetime import date, datetime

import pytest
import pytz
from cornflake.exceptions import ValidationError

from radar.api.serializers.validators import after_day_zero


def test_before():
    with pytest.raises(ValidationError):
        after_day_zero()(date(1899, 12, 31))


def test_on():
    value = after_day_zero()(date(1900, 1, 1))
    assert value == date(1900, 1, 1)


def test_after():
    value = after_day_zero()(date(1900, 1, 2))
    assert value == date(1900, 1, 2)


def test_datetime():
    value = after_day_zero()(datetime(1900, 1, 1, 0, 0, 0, tzinfo=pytz.utc))
    assert value == datetime(1900, 1, 1, 0, 0, 0, tzinfo=pytz.utc)


def test_dt_format():
    with pytest.raises(ValidationError) as e:
        after_day_zero(dt_format='%Y-%m-%d')(datetime(1899, 12, 31, 23, 59, 59, tzinfo=pytz.utc))

    assert e.value.errors[0] == 'Value is before 1900-01-01.'
