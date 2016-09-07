import collections
from datetime import datetime, date, timedelta
from functools import partial
from random import SystemRandom

import inflection
import pytz
import six
from sqlalchemy import and_


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


# TODO this should just return number of months
def seconds_to_age(seconds):
    years = float(seconds) / SECONDS_IN_YEAR

    if years >= 5:
        years = int(years)
    else:
        # Round down to nearest month
        months = int((years - int(years)) * 12) / 12.0
        years = int(years) + months

    return years * SECONDS_IN_YEAR


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
