import re
from datetime import datetime

import pytz
import sqlalchemy
import zxcvbn

from cornflake.fields import ValidationError
from cornflake.validators import after, not_in_future

from radar.constants import HUMAN_DATE_FORMAT
from radar.safe_strftime import safe_strftime
from radar.utils import datetime_to_date, is_datetime

EMAIL_REGEX = re.compile(r'^\S+@[^\.@\s][^@]*\.[^\.@\s]+$')

USERNAME_REGEX = re.compile('^[a-z0-9](?:[a-z0-9]*(?:[\.][a-z0-9]+)?)*$')
USERNAME_MIN_LENGTH = 4
USERNAME_MAX_LENGTH = 32

TRAILING_COMMA_REGEX = re.compile('\s*,$')
TRAILING_SLASH_REGEX = re.compile('.*/$')

DAY_ZERO = datetime(1900, 1, 1, 0, 0, 0, tzinfo=pytz.utc)


def after_day_zero(dt_format=HUMAN_DATE_FORMAT):
    after_f = after(min_dt=DAY_ZERO, dt_format=dt_format)

    def after_day_zero_f(value):
        return after_f(value)

    return after_day_zero_f


class after_date_of_birth(object):
    def __init__(self, field_name, parent=None):
        self.field_name = field_name
        self.parent = parent

    def __call__(self, data):
        field = getattr(self.parent, self.field_name)
        patient_field = getattr(self.parent, 'patient')

        source = field.source
        patient_source = patient_field.source

        value = data.get(source)

        if value is None:
            return data

        patient = data.get(patient_source)

        if patient is None:
            return data

        if is_datetime(value):
            value_date = datetime_to_date(value)
        else:
            value_date = value

        earliest_date_of_birth = patient.earliest_date_of_birth

        if earliest_date_of_birth is not None and value_date < earliest_date_of_birth:
            message = "Value is before the patient's date of birth ({}).".format(
                safe_strftime(earliest_date_of_birth, HUMAN_DATE_FORMAT)
            )

            raise ValidationError({self.field_name: message})

        return data

    def set_context(self, parent):
        self.parent = parent


class valid_date_for_patient(object):
    def __init__(self, field_name, parent=None):
        self.field_name = field_name
        self.parent = parent

    def __call__(self, data):
        source = getattr(self.parent, self.field_name).source
        value = data.get(source)

        if value is None:
            return data

        try:
            value = after_day_zero()(value)
            value = not_in_future()(value)
        except ValidationError as e:
            raise ValidationError({self.field_name: e.errors})

        data[source] = value

        data = after_date_of_birth(self.field_name, self.parent)(data)

        return data

    def set_context(self, parent):
        self.parent = parent


def username():
    def username_f(value):
        value = value.lower()

        # Old usernames are email addresses
        if not EMAIL_REGEX.match(value):
            if not USERNAME_REGEX.match(value):
                raise ValidationError('Not a valid username.')
            elif len(value) < USERNAME_MIN_LENGTH:
                raise ValidationError('Username too short.')
            elif len(value) > USERNAME_MAX_LENGTH:
                raise ValidationError('Username too long.')

        return value

    return username_f


def remove_trailing_comma():
    def remove_trailing_comma_f(value):
        value = TRAILING_COMMA_REGEX.sub('', value)
        return value

    return remove_trailing_comma_f


def sqlalchemy_connection_string():
    def sqlalchemy_connection_string_f(value):
        try:
            sqlalchemy.engine.url.make_url(value)
        except sqlalchemy.exc.ArgumentError:
            raise ValidationError('Not a valid SQLAlchemy connection string.')

        return value

    return sqlalchemy_connection_string_f


def min_crack_time(min_seconds):
    def min_crack_time_f(value):
        seconds = zxcvbn.password_strength(value)['crack_time']

        if seconds < min_seconds:
            raise ValidationError('Crack time of %d seconds is less than minimum of %d seconds.' % (seconds, min_seconds))

        return value

    return min_crack_time_f


def no_trailing_slash():
    def no_trailing_slash_f(value):
        if TRAILING_SLASH_REGEX.match(value):
            raise ValidationError("Shouldn't have a trailing slash.")

        return value

    return no_trailing_slash_f
