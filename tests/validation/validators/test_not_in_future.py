from datetime import date, timedelta, datetime
import pytest
import pytz
from radar.lib.validation.core import ValidationError
from radar.lib.validation.validators import not_in_future


def test_date_past():
    not_in_future()(date.today() - timedelta(days=1))


def test_date_present():
    not_in_future()(date.today())


def test_date_future():
    with pytest.raises(ValidationError):
        # Tomorrow
        not_in_future()(date.today() + timedelta(days=1))


def test_datetime_past():
    not_in_future()(datetime.now(pytz.utc) - timedelta(days=1))


def test_datetime_present():
    not_in_future()(datetime.now(pytz.utc))


def test_datetime_future():
    with pytest.raises(ValidationError):
        not_in_future()(datetime.now(pytz.utc) + timedelta(days=1))
