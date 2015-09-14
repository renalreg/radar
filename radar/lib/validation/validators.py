import re
from datetime import datetime
import pytz

from radar.lib.utils import is_date, date_to_datetime, datetime_to_date, is_datetime
from radar.lib.validation.core import SkipField, ValidationError, pass_context, pass_call
from radar.lib.validation.utils import validate_nhs_no


def required():
    def f(value):
        if value is None:
            raise ValidationError('This field is required.')

        return value

    return f


def optional():
    def f(value):
        if value is None:
            raise SkipField()

        return value

    return f


def after_date_of_birth():
    @pass_context
    def f(ctx, value):
        if is_datetime(value):
            value_date = datetime_to_date(value)
        else:
            value_date = value

        patient = ctx['patient']

        earliest_date_of_birth = patient.earliest_date_of_birth

        if earliest_date_of_birth is not None and value_date < earliest_date_of_birth:
            raise ValidationError("Value is before the patient's date of birth (%s)." % earliest_date_of_birth.strftime('%d/%m/%Y'))

        return value

    return f


def none_if_blank():
    def f(value):
        if value is not None and len(value) == 0:
            value = None

        return value

    return f


def valid_date_for_patient():
    @pass_call
    def f(call, value):
        value = call(after_date_of_birth(), value)
        value = call(not_in_future(), value)
        return value

    return f


def not_empty():
    def f(value):
        if value is None or len(value) == 0:
            raise ValidationError('This field is required.')

        return value

    return f


def min_(min_value):
    def f(value):
        if value < min_value:
            raise ValidationError('Must be greater than or equal to %s.' % min_value)

        return value

    return f


def max_(max_value):
    def f(value):
        if value > max_value:
            raise ValidationError('Must be less than or equal to %s.' % max_value)

        return value

    return f


def range_(min_value=None, max_value=None):
    @pass_call
    def f(call, value):
        if min_value is not None:
            value = call(min_(min_value), value)

        if max_value is not None:
            value = call(max_(max_value), value)

        return value

    return f


def in_(values):
    def f(value):
        if value not in values:
            raise ValidationError('Not a valid value.')

        return value

    return f


def not_in_future():
    def f(value):
        # Convert date to datetime
        if is_date(value):
            value = date_to_datetime(value)

        if value > datetime.now(pytz.utc):
            raise ValidationError("Can't be in the future.")

        return value

    return f


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


def max_length(max_value):
    def f(value):
        if len(value) > max_value:
            raise ValidationError('Value is too long (max length is %d characters).' % max_value)

        return value

    return f


def min_length(min_value):
    def f(value):
        if len(value) < min_value:
            raise ValidationError('Value is too short (min length is %d characters).' % min_value)

        return value

    return f


def email_address():
    def f(value):
        if not re.match(r'^.+@[^.@][^@]*\.[^.@]+$', value):
            raise ValidationError('Not a valid email address.')

        return value

    return f


def _nhs_no(value, number_type):
    if not validate_nhs_no(value):
        raise ValidationError('Not a valid %s number.' % number_type)

    return value


def chi_no():
    def f(value):
        return _nhs_no(value, 'CHI')

    return f


def nhs_no():
    def f(value):
        return _nhs_no(value, 'NHS')

    return f
