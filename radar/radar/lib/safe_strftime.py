import re
from radar.lib.utils import is_date, date_to_datetime

MONTH_NAMES = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

SHORT_MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

SAFE_STRFTIME_DIRECTIVES = {
    '%': lambda x: '%',
    'Y': lambda x: '%04d' % x.year,
    'y': lambda x: ('%04d' % x.year)[-2:],
    'B': lambda x: MONTH_NAMES[x.month - 1],
    'b': lambda x: SHORT_MONTH_NAMES[x.month - 1],
    'm': lambda x: '%02d' % x.month,
    'd': lambda x: '%02d' % x.day,
    'H': lambda x: '%02d' % x.hour,
    'I': lambda x: '%02d' % (x.hour % 12),
    'p': lambda x: 'PM' if x.hour >= 12 else 'AM',
    'M': lambda x: '%02d' % x.minute,
    'S': lambda x: '%02d' % x.second,
    'f': lambda x: '%06d' % x.microsecond,
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
