import collections
from datetime import datetime, date, timedelta
from functools import partial
from random import SystemRandom

import inflection
import pytz
import six
from sqlalchemy import and_
from cornflake.exceptions import SkipField
from dateutil.relativedelta import relativedelta


SECONDS_IN_YEAR = 365 * 24 * 60 * 60


def date_to_datetime(d):
    return datetime(year=d.year, month=d.month, day=d.day, tzinfo=pytz.utc)


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
    return relativedelta(a, b).months


def round_age(months):
    """Remove partial years for ages > 5."""

    # 60 months = 5 years
    if months > 60:
        months = months - (months % 12)

    return months


def random_string(alphabet, length):
    return ''.join(SystemRandom().choice(alphabet) for _ in range(length))


def uniq(items):
    seen = set()
    unique_items = []

    for item in items:
        if item not in seen:
            seen.add(item)
            unique_items.append(item)

    return unique_items


def transform_keys(value, fn):
    if isinstance(value, collections.Mapping):
        value = {fn(k): transform_keys(v, fn) for k, v in value.items()}
    elif isinstance(value, collections.Iterable) and not isinstance(value, six.string_types):
        value = [transform_keys(v, fn) for v in value]

    return value

camel_case = partial(inflection.camelize, uppercase_first_letter=False)
snake_case = partial(inflection.underscore)
camel_case_keys = partial(transform_keys, fn=camel_case)
snake_case_keys = partial(transform_keys, fn=snake_case)


def get_path(data, *path):
    value = data

    for key in path:
        value = value.get(key)

        if value is None:
            break

    return value


def get_attrs(data, *attrs):
    value = data

    for attr in attrs:
        try:
            value = getattr(value, attr)
        except AttributeError:
            value = None

        if value is None:
            break

    return value


class SkipProxy(object):
    def __init__(self, instance):
        self.instance = instance

    def __getattr__(self, item):
        try:
            return getattr(self.instance, item)
        except SkipField:
            return None


def pairwise(values):
    iterator = iter(values)
    return zip(iterator, iterator)
