from datetime import datetime

from radar.lib.utils import date_to_datetime, is_date
from radar.lib.validation.core import ValidationError, StopValidation


def required(value):
    if value is None:
        raise ValidationError('This field is required.')


def optional(value):
    if value is None:
        raise StopValidation()


def not_empty(value):
    if value is None or len(value) == 0:
        raise ValidationError('This field is required.')


def min_(min_value):
    def f(value):
        if value < min_value:
            raise ValidationError('Must be greater than or equal to %s.' % min_value)

    return f


def max_(max_value):
    def f(value):
        if value > max_value:
            raise ValidationError('Must be less than or equal to %s.' % max_value)

    return f


def range_(min_value=None, max_value=None):
    def f(value):
        if min_value is not None:
            min_(min_value)(value)

        if max_value is not None:
            max_(max_value)(value)

    return f


def in_(values):
    def f(value):
        if value not in values:
            raise ValidationError('Not a valid value.')

    return f


def not_in_future(value):
    # Convert date to datetime
    if is_date(value):
        value = date_to_datetime(value)

    if value > datetime.now():
        raise ValidationError("Can't be in the future.")


def after(min_dt, dt_format='%d/%m/%Y'):
    if is_date(min_dt):
        min_dt = date_to_datetime(min_dt)

    def f(value):
        if is_date(value):
            value = date_to_datetime(value)

        if value < min_dt:
            raise ValidationError('Value is before %s.' % min_dt.strftime(dt_format))

    return f


def before(max_dt, dt_format='%d/%m/%Y'):
    if is_date(max_dt):
        max_dt = date_to_datetime(max_dt)

    def f(value):
        if is_date(value):
            value = date_to_datetime(value)

        if value > max_dt:
            raise ValidationError('Value is after %s.' % max_dt.strftime(dt_format))

    return f
