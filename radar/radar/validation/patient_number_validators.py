import re

from radar.validation.core import ValidationError
from radar.models import ORGANISATION_CODE_NHS, ORGANISATION_CODE_CHI, ORGANISATION_CODE_HANDC, \
    ORGANISATION_CODE_UKRR, ORGANISATION_CODE_UKRDC, ORGANISATION_CODE_BAPN

WHITESPACE_REGEX = re.compile('\s')
LEADING_ZERO_REGEX = re.compile('^0+')
DIGITS_REGEX = re.compile('^[0-9]+$')

MIN_UKRR_NO = 199600001
MAX_UKRR_NO = 999999999

BAPN_NO_REGEX = re.compile('^[ABCDFGHJKLMNPT][0-9]{,3}$')
BAPN_LEADING_ZEROS = re.compile('^[A-Z](0+)')

MIN_UKRDC_NO = 100000001
MAX_UKRDC_NO = 999999999


def clean_int(value):
    if isinstance(value, basestring):
        # Remove non-digits
        value = re.sub('[^0-9]', '', value)

        # Remove leading zeros
        value = re.sub('^0+', '', value)

    return value


def validate_nhs_no(value):
    if not isinstance(value, basestring):
        value = str(value)

    value = value.zfill(10)

    if not value.isdigit():
        return False

    check_digit = 0

    for i in range(0, 9):
        check_digit += int(value[i]) * (10 - i)

    check_digit = 11 - (check_digit % 11)

    if check_digit == 11:
        check_digit = 0

    if check_digit != int(value[9]):
        return False

    return True


def _nhs_no(value, number_type):
    value = clean_int(value)

    if not validate_nhs_no(value):
        raise ValidationError('Not a valid %s number.' % number_type)

    return value


# TODO range
def nhs_no():
    def nhs_no_f(value):
        return _nhs_no(value, 'NHS')

    return nhs_no_f


# TODO range
def chi_no():
    def chi_no_f(value):
        return _nhs_no(value, 'CHI')

    return chi_no_f


# TODO range
def handc_no():
    def handc_no_f(value):
        return _nhs_no(value, 'H&C')

    return handc_no_f


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
        if isinstance(value, basestring):
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


NUMBER_VALIDATORS = {
    ORGANISATION_CODE_NHS: [nhs_no()],
    ORGANISATION_CODE_CHI: [chi_no()],
    ORGANISATION_CODE_HANDC: [handc_no()],
    ORGANISATION_CODE_UKRR: [ukrr_no()],
    ORGANISATION_CODE_UKRDC: [ukrdc_no()],
    ORGANISATION_CODE_BAPN: [bapn_no()]
}
