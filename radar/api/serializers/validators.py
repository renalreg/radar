from datetime import datetime
import re

from cornflake.fields import ValidationError
from cornflake.utils import safe_strftime
from cornflake.validators import after, not_in_future
import pytz

from radar.models.groups import (
    GROUP_CODE_BAPN,
    GROUP_CODE_CHI,
    GROUP_CODE_HSC,
    GROUP_CODE_NHS,
    GROUP_CODE_RADAR,
    GROUP_CODE_UKRDC,
    GROUP_CODE_UKRR,
    GROUP_TYPE,
)
from radar.models.patients import Patient
from radar.utils import datetime_to_date, is_datetime


HUMAN_DATE_FORMAT = '%d/%m/%Y'

EMAIL_REGEX = re.compile(r'^\S+@[^\.@\s][^@]*\.[^\.@\s]+$')

USERNAME_REGEX = re.compile(r'^[a-z0-9](?:[a-z0-9]*(?:[\.][a-z0-9]+)?)*$')
USERNAME_MIN_LENGTH = 4
USERNAME_MAX_LENGTH = 32

TRAILING_COMMA_REGEX = re.compile(r'\s*,$')

DAY_ZERO = datetime(1900, 1, 1, 0, 0, 0, tzinfo=pytz.utc)

WHITESPACE_REGEX = re.compile(r'\s')
LEADING_ZERO_REGEX = re.compile(r'^0+')
DIGITS_REGEX = re.compile(r'^[0-9]+$')

MIN_UKRR_NO = 199600001
MAX_UKRR_NO = 999999999

BAPN_NO_REGEX = re.compile(r'^[ABCDFGHJKLMNPT][0-9]{,3}$')
BAPN_LEADING_ZEROS = re.compile(r'^[A-Z](0+)')

MIN_UKRDC_NO = 100000001
MAX_UKRDC_NO = 999999999

MIN_GMC_NO = 0
MAX_GMC_NO = 9999999

MIN_NHS_NO = 4000000000

MIN_CHI_NO = 101000000
MAX_CHI_NO = 3112999999

MIN_HSC_NO = 3200000010
MAX_HSC_NO = 3999999999


def after_day_zero(dt_format=HUMAN_DATE_FORMAT):
    after_f = after(min_dt=DAY_ZERO, dt_format=dt_format)

    def after_day_zero_f(value):
        return after_f(value)

    return after_day_zero_f


class after_date_of_birth(object):
    def __init__(self, field_name, patient='patient', parent=None):
        self.field_name = field_name
        self.patient = patient
        self.parent = parent

    def __call__(self, data):
        field = self.parent.fields[self.field_name]

        value = field.get_attribute(data)

        if value is None:
            return data

        if callable(self.patient):
            patient = self.patient()
        elif isinstance(self.patient, Patient):
            patient = self.patient
        else:
            patient_field = self.parent.fields[self.patient]
            patient = patient_field.get_attribute(data)

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
    def __init__(self, field_name, patient='patient', parent=None):
        self.field_name = field_name
        self.patient = patient
        self.parent = parent

    def __call__(self, data):
        field = self.parent.fields[self.field_name]
        value = field.get_attribute(data)

        # Exit early if value is none
        if value is None:
            return data

        try:
            # Not a long way in the past
            value = after_day_zero()(value)

            # Not in the future
            value = not_in_future()(value)
        except ValidationError as e:
            raise ValidationError({self.field_name: e.errors})

        data[field.source] = value

        # After the patient's date of birth
        data = after_date_of_birth(self.field_name, self.patient, self.parent)(data)

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
        # Remove a trailing comma
        value = TRAILING_COMMA_REGEX.sub('', value)
        return value

    return remove_trailing_comma_f


def clean_int(value):
    if isinstance(value, str):
        # Remove non-digits
        value = re.sub('[^0-9]', '', value)

        # Remove leading zeros
        value = re.sub('^0+', '', value)

    return value


def check_range(value, min_value=None, max_value=None):
    if isinstance(value, str):
        value = int(value)

    # min_value <= x <= max_value
    return (
        (min_value is None or value >= min_value) and
        (max_value is None or value <= max_value)
    )


def _nhs_no(value, min_value=None, max_value=None):
    if not isinstance(value, str):
        value = str(value)

    # Remove non-digits
    value = re.sub('[^0-9]', '', value)

    if len(value) > 10:
        # Remove extra leading zeros
        if re.match('^0+$', value[0:-10]):
            value = value[-10:]
    elif len(value) < 10:
        # Add leading zeros
        value = value.zfill(10)

    if len(value) != 10:
        raise ValueError('Not 10 digits.')

    check_digit = 0

    for i in range(0, 9):
        check_digit += int(value[i]) * (10 - i)

    check_digit = 11 - (check_digit % 11)

    if check_digit == 11:
        check_digit = 0

    if check_digit != int(value[9]):
        raise ValueError('Bas check digit.')

    if not check_range(value, min_value, max_value):
        raise ValueError('Not in range.')

    return value


def nhs_no():
    def nhs_no_f(value):
        try:
            new_value = _nhs_no(value, MIN_NHS_NO)
        except ValueError:
            raise ValidationError('Not a valid NHS number.')

        if isinstance(value, str):
            value = new_value

        return value

    return nhs_no_f


def chi_no():
    def chi_no_f(value):
        try:
            new_value = _nhs_no(value, MIN_CHI_NO, MAX_CHI_NO)
        except ValueError:
            raise ValidationError('Not a valid CHI number.')

        if isinstance(value, str):
            value = new_value

        return value

    return chi_no_f


def hsc_no():
    def hsc_no_f(value):
        try:
            new_value = _nhs_no(value, MIN_HSC_NO, MAX_HSC_NO)
        except ValueError:
            raise ValidationError('Not a valid H&C number.')

        if isinstance(value, str):
            value = new_value

        return value

    return hsc_no_f


def ukrr_no():
    def ukrr_no_f(value):
        value = clean_int(value)

        try:
            x = int(value)
        except ValueError:
            raise ValidationError('Not a valid UK Renal Registry number.')

        if x < MIN_UKRR_NO or x > MAX_UKRR_NO:
            raise ValidationError('Not a valid UK Renal Registry number.')

        return value

    return ukrr_no_f


def nhsbt_no():
    def nhsbt_no_f(value):
        if isinstance(value, str):
            # Remove leading zeros and whitespace
            value = LEADING_ZERO_REGEX.sub('', value)
            value = WHITESPACE_REGEX.sub('', value)

            if not DIGITS_REGEX.match(value):
                raise ValidationError('Not a valid NHS Blood and Tracing number.')

        return value

    return nhsbt_no_f


def bapn_no():
    def bapn_no_f(value):
        value = value.upper()
        value = re.sub('[^A-Z0-9]', '', value)

        if not BAPN_NO_REGEX.match(value):
            raise ValidationError('Not a valid BAPN number.')

        # Remove leading zeros
        value = BAPN_LEADING_ZEROS.sub('', value)

        return value

    return bapn_no_f


def ukrdc_no():
    def ukrdc_no_f(value):
        value = clean_int(value)

        try:
            x = int(value)
        except ValueError:
            raise ValidationError('Not a valid UKRDC number.')

        if x < MIN_UKRDC_NO or x > MAX_UKRDC_NO:
            raise ValidationError('Not a valid UKRDC number.')

        return value

    return ukrdc_no_f


def gmc_number():
    def gmc_number_f(value):
        value = clean_int(value)

        try:
            x = int(value)
        except ValueError:
            raise ValidationError('Not a valid GMC number.')

        if x < MIN_GMC_NO or x > MAX_GMC_NO:
            raise ValidationError('Not a valid GMC number.')

        return value

    return gmc_number_f


def radar_no():
    def radar_no_f(value):
        value = clean_int(value)

        try:
            int(value)
        except ValueError:
            raise ValidationError('Not a valid RaDaR number.')

        return value

    return radar_no_f


NUMBER_VALIDATORS = {
    (GROUP_TYPE.OTHER, GROUP_CODE_NHS): [nhs_no()],
    (GROUP_TYPE.OTHER, GROUP_CODE_CHI): [chi_no()],
    (GROUP_TYPE.OTHER, GROUP_CODE_HSC): [hsc_no()],
    (GROUP_TYPE.OTHER, GROUP_CODE_UKRR): [ukrr_no()],
    (GROUP_TYPE.OTHER, GROUP_CODE_UKRDC): [ukrdc_no()],
    (GROUP_TYPE.OTHER, GROUP_CODE_BAPN): [bapn_no()],
    (GROUP_TYPE.SYSTEM, GROUP_CODE_RADAR): [radar_no()],
}


def get_number_validators(group):
    return NUMBER_VALIDATORS.get((group.type, group.code), [])
