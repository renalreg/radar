import re
from radar.lib.utils import is_date, date_to_datetime

SAFE_STRFTIME_DIRECTIVES = {
    '%': lambda x: '%',
    'Y': lambda x: '%04d' % x.year,
    'y': lambda x: ('%04d' % x.year)[-2:],
    'm': lambda x: '%02d' % x.month,
    'd': lambda x: '%02d' % x.day,
    'H': lambda x: '%02d' % x.hour,
    'I': lambda x: '%02d' % (x.hour % 12),
    'M': lambda x: '%02d' % x.minute,
    'S': lambda x: '%02d' % x.second,
}


def safe_strftime_replace(dt, directive):
    try:
        f = SAFE_STRFTIME_DIRECTIVES[directive]
    except KeyError:
        raise ValueError('Invalid format string')

    return f(dt)


def safe_strftime(value, format):
    if is_date(value):
        value_dt = date_to_datetime(value)
    else:
        value_dt = value

    return re.sub('%(.)', lambda x: safe_strftime_replace(value_dt, x.group(1)), format)
