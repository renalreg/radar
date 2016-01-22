import re
import itertools

MIN_NHS_NO = '4000000000'

MIN_CHI_NO = '0101000000'
MAX_CHI_NO = '3112999999'

MIN_HANDC_NO = '3200000010'
MAX_HANDC_NO = '3999999999'


def nhs_no(value):
    return _nhs_no(value, MIN_NHS_NO)


def chi_no(value):
    return _nhs_no(value, MIN_CHI_NO, MAX_CHI_NO)


def handc_no(value):
    return _nhs_no(value, MIN_HANDC_NO, MAX_HANDC_NO)


def _nhs_no(value, min_value=None, max_value=None):
    if not isinstance(value, basestring):
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
        raise ValueError('Not a 10 digit number')

    check_digit = 0

    for i in range(0, 9):
        check_digit += int(value[i]) * (10 - i)

    check_digit = 11 - (check_digit % 11)

    if check_digit == 11:
        check_digit = 0

    if check_digit != int(value[9]):
        raise ValueError('Incorrect check digit')

    if (
        (min_value is not None and value < min_value) or
        (max_value is not None and value > max_value)
    ):
        raise ValueError('Not in range')

    return value


def grouper(n, iterable):
    it = iter(iterable)

    while True:
        chunk = tuple(itertools.islice(it, n))

        if not chunk:
            return

        yield chunk
