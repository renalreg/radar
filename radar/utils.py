import collections.abc
from datetime import date, datetime, timedelta
from functools import partial
from random import SystemRandom

from cornflake.exceptions import SkipField
from dateutil.relativedelta import relativedelta
import inflection
import pytz
from sqlalchemy import and_


SECONDS_IN_YEAR = 365 * 24 * 60 * 60


def date_to_datetime(d, with_timezone=True):
    if with_timezone:
        return datetime(year=d.year, month=d.month, day=d.day, tzinfo=pytz.utc)
    else:
        return datetime(year=d.year, month=d.month, day=d.day)


def is_date(x):
    return isinstance(x, date) and not isinstance(x, datetime)


def is_datetime(x):
    return isinstance(x, datetime)


def datetime_to_date(dt):
    return date(dt.year, dt.month, dt.day)


def sql_date_filter(column, date):
    return and_(
        column >= date,
        column < date + timedelta(days=1)
    )


def sql_year_filter(column, year):
    return and_(
        column >= datetime(year, 1, 1),
        column < datetime(year + 1, 1, 1)
    )


def months_between(a, b):
    """Number of months between two dates."""

    delta = relativedelta(a, b)
    return delta.years * 12 + delta.months


def round_age(months):
    """Remove partial years for ages > 5."""

    # 60 months = 5 years
    if months > 60:
        months = months - (months % 12)

    return months


def random_string(alphabet, length):
    """Random string from an alphabet."""

    return ''.join(SystemRandom().choice(alphabet) for _ in range(length))


def uniq(items):
    """Unique items in a list."""

    seen = set()
    unique_items = []

    for item in items:
        if item not in seen:
            seen.add(item)
            unique_items.append(item)

    return unique_items


def transform_keys(value, fn):
    """Recursively transform the keys of the supplied value."""
    if isinstance(value, collections.abc.Mapping):
        value = {fn(str(k)): transform_keys(v, fn) for k, v in value.items()}
    elif isinstance(value, collections.abc.Iterable) and not isinstance(value, str):
        value = [transform_keys(v, fn) for v in value]

    return value


camel_case = partial(inflection.camelize, uppercase_first_letter=False)
snake_case = partial(inflection.underscore)
camel_case_keys = partial(transform_keys, fn=camel_case)
snake_case_keys = partial(transform_keys, fn=snake_case)


def get_path(data, *path):
    """Get the dictionary value at the supplied path."""

    value = data

    for key in path:
        if value is None:
            break

        value = value.get(key)

    return value


def get_attrs(data, *attrs):
    """Get the object value at the supplied path."""

    value = data

    for attr in attrs:
        if value is None:
            break

        try:
            value = getattr(value, attr)
        except AttributeError:
            if isinstance(value, dict):
                value = value.get(attr)
            else:
                value = None

    return value


class SkipProxy(object):
    """Catch SkipField exceptions and return None instead."""

    def __init__(self, instance):
        self.instance = instance

    def __getattr__(self, item):
        try:
            return getattr(self.instance, item)
        except SkipField:
            return None


def pairwise(values):
    """Group values in a list into pairs."""

    iterator = iter(values)
    return zip(iterator, iterator)
