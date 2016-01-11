import re

from radar.validation.core import ValidationError
from radar.models.groups import GROUP_CODE_NHS, GROUP_CODE_CHI, GROUP_CODE_HANDC, \
    GROUP_CODE_UKRR, GROUP_CODE_UKRDC, GROUP_CODE_BAPN

WHITESPACE_REGEX = re.compile('\s')
LEADING_ZERO_REGEX = re.compile('^0+')
DIGITS_REGEX = re.compile('^[0-9]+$')

MIN_UKRR_NO = 199600001
MAX_UKRR_NO = 999999999

BAPN_NO_REGEX = re.compile('^[ABCDFGHJKLMNPT][0-9]{,3}$')
BAPN_LEADING_ZEROS = re.compile('^[A-Z](0+)')

MIN_UKRDC_NO = 100000001
MAX_UKRDC_NO = 999999999

MIN_GMC_NO = 0
MAX_GMC_NO = 9999999

MIN_NHS_NO = 4000000000

MIN_CHI_NO = 0101000000
MAX_CHI_NO = 3112999999

MIN_HANDC_NO = 3200000010
MAX_HANDC_NO = 3999999999


def clean_int(value):
    if isinstance(value, basestring):
        # Remove non-digits
        value = re.sub('[^0-9]', '', value)

        # Remove leading zeros
        value = re.sub('^0+', '', value)

    return value


def check_range(value, min_value=None, max_value=None):
    if isinstance(value, basestring):
        value = int(value)

    return (
        (min_value is None or value >= min_value) and
        (max_value is None or value <= max_value)
    )


def check_number(value, min_value=None, max_value=None):
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

    if not check_range(value, min_value, max_value):
        return False

    return True


def nhs_no():
    def nhs_no_f(value):
        value = clean_int(value)

        if not check_number(value, MIN_NHS_NO):
            raise ValidationError('Not a valid NHS number.')

        return value

    return nhs_no_f


def chi_no():
    def chi_no_f(value):
        value = clean_int(value)

        if not check_number(value, MIN_CHI_NO, MAX_CHI_NO):
            raise ValidationError('Not a valid CHI number.')

        return value

    return chi_no_f


def handc_no():
    def handc_no_f(value):
        value = clean_int(value)

        if not check_number(value, MIN_HANDC_NO, MAX_HANDC_NO):
            raise ValidationError('Not a valid H&C number.')

        return value

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


NUMBER_VALIDATORS = {
    GROUP_CODE_NHS: [nhs_no()],
    GROUP_CODE_CHI: [chi_no()],
    GROUP_CODE_HANDC: [handc_no()],
    GROUP_CODE_UKRR: [ukrr_no()],
    GROUP_CODE_UKRDC: [ukrdc_no()],
    GROUP_CODE_BAPN: [bapn_no()]
}
