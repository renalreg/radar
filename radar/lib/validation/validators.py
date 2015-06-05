from datetime import datetime

from radar.lib.utils import date_to_datetime, is_date


def required(value):
    if value is None:
        return 'This field is required.'


def not_empty(value):
    if value is None or len(value) == 0:
        return 'This field is required.'


def min_(min_value):
    def f(value):
        if value < min_value:
            return 'Must be greater than or equal to %s.' % min_value

    return f


def max_(max_value):
    def f(value):
        if value > max_value:
            return 'Must be less than or equal to %s.' % max_value

    return f


def range_(min_value=None, max_value=None):
    def f(value):
        if min_value is not None:
            r = min_(min_value)(value)

            if r is not None:
                return r

        if max_value is not None:
            r = max_(max_value)(value)

            if r is not None:
                return r

    return f


def in_(values):
    def f(value):
        if value not in values:
            return 'Not a valid value.'

    return f


def not_in_future(value):
    # Convert date to datetime
    if is_date(value):
        value = date_to_datetime(value)

    if value > datetime.now():
        return "Can't be in the future."


def after(min_dt, dt_format='%d/%m/%Y'):
    if is_date(min_dt):
        min_dt = date_to_datetime(min_dt)

    def f(value):
        if is_date(value):
            value = date_to_datetime(value)

        if value < min_dt:
            return 'Value is before %s.' % value.strftime(dt_format)

    return f


def before(max_dt, dt_format='%d/%m/%Y'):
    if is_date(max_dt):
        max_dt = date_to_datetime(max_dt)

    def f(value):
        if is_date(value):
            value = date_to_datetime(value)

        if value > max_dt:
            return 'Value is after %s.' % value.strftime(dt_format)

    return f
