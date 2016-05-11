from datetime import datetime, date, timedelta
from random import SystemRandom

from sqlalchemy import and_
import pytz


SECONDS_IN_YEAR = 365 * 24 * 60 * 60


def date_to_datetime(d):
    dt = datetime(year=d.year, month=d.month, day=d.day)
    dt = pytz.timezone('Europe/London').localize(dt)
    return dt


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
