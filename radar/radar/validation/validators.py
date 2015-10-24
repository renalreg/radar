import re
from datetime import datetime, date

import pytz
import sqlalchemy
import zxcvbn

from radar.constants import HUMAN_DATE_FORMAT
from radar.safe_strftime import safe_strftime
from radar.utils import is_date, date_to_datetime, datetime_to_date, is_datetime
from radar.validation.core import SkipField, ValidationError, pass_context, pass_call


USERNAME_REGEX = re.compile('^[a-z0-9](?:[a-z0-9]*(?:[\.][a-z0-9]+)?)*$')
USERNAME_MIN_LENGTH = 4
USERNAME_MAX_LENGTH = 32

PASSWORD_MIN_LENGTH = 8

EMAIL_REGEX = re.compile(r'^.+@[^.@][^@]*\.[^.@]+$')

POSTCODE_BFPO_REGEX = re.compile('^BFPO[ ]?\\d{1,4}$')
POSTCODE_REGEX = re.compile('^(GIR[ ]?0AA|((AB|AL|B|BA|BB|BD|BH|BL|BN|BR|BS|BT|BX|CA|CB|CF|CH|CM|CO|CR|CT|CV|CW|DA|DD|DE|DG|DH|DL|DN|DT|DY|E|EC|EH|EN|EX|FK|FY|G|GL|GY|GU|HA|HD|HG|HP|HR|HS|HU|HX|IG|IM|IP|IV|JE|KA|KT|KW|KY|L|LA|LD|LE|LL|LN|LS|LU|M|ME|MK|ML|N|NE|NG|NN|NP|NR|NW|OL|OX|PA|PE|PH|PL|PO|PR|RG|RH|RM|S|SA|SE|SG|SK|SL|SM|SN|SO|SP|SR|SS|ST|SW|SY|TA|TD|TF|TN|TQ|TR|TS|TW|UB|W|WA|WC|WD|WF|WN|WR|WS|WV|YO|ZE)(\\d[\\dA-Z]?[ ]?\\d[ABD-HJLN-UW-Z]{2}))|BFPO[ ]?\\d{1,4})$')  # noqa

TRAILING_COMMA_REGEX = re.compile('\s*,$')

TAB_TO_SPACE_REGEX = re.compile('\t')
NORMALISE_WHITESPACE_REGEX = re.compile('\s{2,}')

DAY_ZERO = datetime(1900, 1, 1, 0, 0, 0, tzinfo=pytz.utc)


def required():
    def required_f(value):
        if value is None:
            raise ValidationError('This field is required.')

        return value

    return required_f


def optional():
    def optional_f(value):
        if value is None:
            raise SkipField()

        return value

    return optional_f


def after_date_of_birth():
    @pass_context
    def after_date_of_birth_f(ctx, value):
        if is_datetime(value):
            value_date = datetime_to_date(value)
        else:
            value_date = value

        patient = ctx['patient']

        earliest_date_of_birth = patient.earliest_date_of_birth

        if earliest_date_of_birth is not None and value_date < earliest_date_of_birth:
            raise ValidationError("Value is before the patient's date of birth (%s)." % safe_strftime(earliest_date_of_birth, HUMAN_DATE_FORMAT))

        return value

    return after_date_of_birth_f


def none_if_blank():
    def none_if_blank_f(value):
        if value is not None and len(value) == 0:
            value = None

        return value

    return none_if_blank_f


def valid_date_for_patient():
    @pass_call
    def valid_date_for_patient_f(call, value):
        value = call(after_day_zero(), value)
        value = call(not_in_future(), value)
        value = call(after_date_of_birth(), value)
        return value

    return valid_date_for_patient_f


def not_empty():
    def not_empty_f(value):
        if value is None or len(value) == 0:
            raise ValidationError('This field is required.')

        return value

    return not_empty_f


def min_(min_value):
    def min_f(value):
        if value < min_value:
            raise ValidationError('Must be greater than or equal to %s.' % min_value)

        return value

    return min_f


def max_(max_value):
    def max_f(value):
        if value > max_value:
            raise ValidationError('Must be less than or equal to %s.' % max_value)

        return value

    return max_f


def range_(min_value=None, max_value=None):
    @pass_call
    def range_f(call, value):
        if min_value is not None:
            value = call(min_(min_value), value)

        if max_value is not None:
            value = call(max_(max_value), value)

        return value

    return range_f


def in_(values):
    def in_f(value):
        if value not in values:
            raise ValidationError('Not a valid value.')

        return value

    return in_f


def not_in_future():
    def not_in_future_f(value):
        if is_date(value):
            now = date.today()
        else:
            now = datetime.now(pytz.utc)

        if value > now:
            raise ValidationError("Can't be in the future.")

        return value

    return not_in_future_f


def after(min_dt, dt_format=HUMAN_DATE_FORMAT):
    if is_date(min_dt):
        min_dt = date_to_datetime(min_dt)

    def after_f(value):
        if is_date(value):
            value_dt = date_to_datetime(value)
        else:
            value_dt = value

        if value_dt < min_dt:
            raise ValidationError('Value is before %s.' % safe_strftime(min_dt, dt_format))

        return value

    return after_f


def before(max_dt, dt_format=HUMAN_DATE_FORMAT):
    if is_date(max_dt):
        max_dt = date_to_datetime(max_dt)

    def before_f(value):
        if is_date(value):
            value_dt = date_to_datetime(value)
        else:
            value_dt = value

        if value_dt > max_dt:
            raise ValidationError('Value is after %s.' % safe_strftime(max_dt, dt_format))

        return value

    return before_f


def max_length(max_value):
    def max_length_f(value):
        if len(value) > max_value:
            raise ValidationError('Value is too long (max length is %d characters).' % max_value)

        return value

    return max_length_f


def min_length(min_value):
    def min_length_f(value):
        if len(value) < min_value:
            raise ValidationError('Value is too short (min length is %d characters).' % min_value)

        return value

    return min_length_f


def email_address():
    def email_address_f(value):
        value = value.lower()

        if not EMAIL_REGEX.match(value):
            raise ValidationError('Not a valid email address.')

        return value

    return email_address_f


def username():
    def username_f(value):
        value = value.lower()

        message = None

        if not USERNAME_REGEX.match(value):
            message = 'Not a valid username.'
        elif len(value) < USERNAME_MIN_LENGTH:
            message = 'Username too short.'
        elif len(value) > USERNAME_MAX_LENGTH:
            message = 'Username too long.'

        # Old usernames are email addresses
        if message is not None and not EMAIL_REGEX.match(value):
            raise ValidationError(message)

        return value

    return username_f


# TODO
def password():
    def password_f(value):
        if len(value) < PASSWORD_MIN_LENGTH:
            raise ValidationError('Password too short (must be at least %d characters).' % PASSWORD_MIN_LENGTH)

        return value

    return password_f


def postcode():
    def postcode_f(value):
        value = value.upper()
        value = re.sub('[^A-Z0-9]', '', value)

        if not POSTCODE_REGEX.match(value):
            raise ValidationError('Not a valid postcode.')

        if POSTCODE_BFPO_REGEX.match(value):
            value = value[:-4] + ' ' + value[-4:]
        else:
            value = value[:-3] + ' ' + value[-3:]

        return value

    return postcode_f


def remove_trailing_comma():
    def remove_trailing_comma_f(value):
        value = TRAILING_COMMA_REGEX.sub('', value)
        return value

    return remove_trailing_comma_f


def normalise_whitespace():
    def normalise_whitespace_f(value):
        # Tabs to spaces
        value = TAB_TO_SPACE_REGEX.sub(' ', value)

        # Multiple spaces
        value = NORMALISE_WHITESPACE_REGEX.sub(' ', value)

        return value

    return normalise_whitespace_f


def upper():
    def upper_f(value):
        value = value.upper()
        return value

    return upper_f


def lower():
    def lower_f(value):
        value = value.lower()
        return value

    return lower_f


def after_day_zero(dt_format=HUMAN_DATE_FORMAT):
    after_f = after(min_dt=DAY_ZERO, dt_format=dt_format)

    def after_day_zero_f(value):
        return after_f(value)

    return after_day_zero_f


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


# TODO
def url():
    def url_f(value):
        return value

    return url_f


# TODO
def no_trailing_slash():
    def no_trailing_slash_f(value):
        return value

    return no_trailing_slash_f
