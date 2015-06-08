from datetime import date, timedelta, datetime

import pytest

from radar.lib.validation.core import ValidationError, StopValidation
from radar.lib.validation.validators import required, not_empty, min_, max_, range_, in_, not_in_future, before, after, \
    optional


def test_required_str():
    required('hello')


def test_required_int():
    required(123)


def test_required_empty():
    required('')


def test_required_none():
    with pytest.raises(ValidationError):
        required(None)


def test_not_empty_str():
    not_empty('hello')


def test_not_empty_list():
    not_empty(['hello', 'world'])


def test_not_empty_empty_str():
    with pytest.raises(ValidationError):
        not_empty('')


def test_not_empty_empty_list():
    with pytest.raises(ValidationError):
        not_empty([])


def test_min_less_than():
    with pytest.raises(ValidationError):
        min_(10)(9)


def test_min_equal():
    min_(10)(10)


def test_min_greater_than():
    min_(10)(11)


def test_max_less_than():
    max_(10)(9)


def test_max_equal():
    max_(10)(10)


def test_max_greater_than():
    with pytest.raises(ValidationError):
        max_(10)(11)


def test_range_min_less_than():
    with pytest.raises(ValidationError):
        range_(min_value=10)(9)


def test_range_min_equal():
    range_(min_value=10)(10)


def test_range_min_greater_than():
    range_(min_value=10)(11)


def test_range_max_less_than():
    range_(max_value=10)(9)


def test_range_max_equal():
    range_(max_value=10)(10)


def test_range_max_greater_than():
    with pytest.raises(ValidationError):
        range_(max_value=10)(11)


def test_range_min_max_less_than():
    with pytest.raises(ValidationError):
        range_(10, 20)(5)


def test_range_min_max_equal_min():
    range_(10, 20)(10)


def test_range_min_max_middle():
    range_(10, 20)(15)


def test_range_min_max_equal_max():
    range_(10, 20)(20)


def test_range_min_max_greater_than():
    with pytest.raises(ValidationError):
        range_(10, 20)(21)


def test_in_in_list():
    in_([1, 2, 3])(1)


def test_in_not_in_list():
    with pytest.raises(ValidationError):
        in_([1, 2, 3])(4)


def test_not_in_future_date_past():
    not_in_future(date.today() - timedelta(days=1))


def test_not_in_future_date_present():
    not_in_future(date.today())


def test_not_in_future_date_future():
    with pytest.raises(ValidationError):
        # Tomorrow
        not_in_future(date.today() + timedelta(days=1))


def test_not_in_future_datetime_past():
    not_in_future(datetime.now() - timedelta(days=1))


def test_not_in_future_datetime_present():
    not_in_future(datetime.now())


def test_not_in_future_datetime_future():
    with pytest.raises(ValidationError):
        not_in_future(datetime.now() + timedelta(days=1))


def test_before_date_datetime():
    before(date(2015, 1, 1))(datetime(2014, 12, 31, 23, 59, 59))


def test_before_datetime_date():
    before(datetime(2015, 1, 1, 0, 0, 0))(date(2014, 12, 31))


def test_before_less_than():
    before(datetime(2015, 1, 1, 0, 0, 0))(datetime(2014, 12, 31, 23, 59, 59))


def test_before_equal():
    before(datetime(2015, 1, 1, 0, 0, 0))(datetime(2015, 1, 1, 0, 0, 0))


def test_before_greater_than():
    with pytest.raises(ValidationError):
        before(datetime(2015, 1, 1, 0, 0, 0))(datetime(2015, 1, 1, 0, 0, 1))


def test_before_dt_format():
    with pytest.raises(ValidationError) as e:
        before(datetime(2015, 1, 1, 0, 0, 0), dt_format='%Y-%m-%d')(datetime(2015, 1, 2, 0, 0, 0))

    assert e.value.message == 'Value is after 2015-01-01.'


def test_after_date_datetime():
    after(date(2015, 1, 1))(datetime(2015, 1, 1, 0, 0, 0))


def test_after_datetime_date():
    after(datetime(2015, 1, 1, 0, 0, 0))(date(2015, 1, 1))


def test_after_less_than():
    with pytest.raises(ValidationError):
        after(datetime(2015, 1, 1, 0, 0, 0))(datetime(2014, 12, 31, 23, 59, 59))


def test_after_equal():
    after(datetime(2015, 1, 1, 0, 0, 0))(datetime(2015, 1, 1, 0, 0, 0))


def test_after_greater_than():
    after(datetime(2015, 1, 1, 0, 0, 0))(datetime(2015, 1, 1, 0, 0, 1))


def test_after_dt_format():
    with pytest.raises(ValidationError) as e:
        after(datetime(2015, 1, 1, 0, 0, 0), dt_format='%Y-%m-%d')(datetime(2014, 12, 31, 0, 0, 0))

    assert e.value.message == 'Value is before 2015-01-01.'


def test_optional_none():
    with pytest.raises(StopValidation) as e:
        optional(None)


def test_optional_empty():
    optional('')


def test_optional_str():
    optional('hello')
