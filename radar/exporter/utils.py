from datetime import date, datetime
import re

from radar.utils import get_attrs

try:
    basestring
except NameError:
    basestring = str
    unicode = str


def get_years(months):
    """Get whole number of years."""

    if months is None:
        years = 0
    else:
        years = months // 12

    return years


def get_months(months):
    """Get remaining months."""

    if months is None:
        months = 0
    else:
        months = months % 12

    return months


def path_getter(path):
    """Get attributes at the dot-separated path."""

    parts = path.split('.')

    def f(value):
        return get_attrs(value, *parts)

    return f


def none_getter(value):
    return None


def identity_getter(value):
    return value


def stringify_list(name):
    def stringify(entry):
        items = entry.data.get(name) or []
        return '; '.join(sorted(items))

    return stringify


def format_user(user):
    if user is None:
        return None
    elif user.first_name and user.last_name:
        return '%s %s' % (user.first_name, user.last_name)
    else:
        return user.username


def format_date(dt):
    val = dt
    fmt = '%d/%m/%Y'
    if isinstance(dt, (date, datetime)):
        try:
            val = dt.strftime(fmt)
        except ValueError:
            val = '{:02d}/{:02d}/{}'.format(dt.day, dt.month, dt.year)
    elif re.match(r'^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$', unicode(dt)):
        try:
            parsed = datetime.strptime(dt, '%Y-%m-%d')
        except ValueError:
            year, month, day = dt.split('-')
            parsed = date(int(year), int(month), int(day))
        try:
            val = parsed.strftime(fmt)
        except ValueError:
            val = '{:02d}/{:02d}/{}'.format(parsed.day, parsed.month, parsed.year)

    return val
