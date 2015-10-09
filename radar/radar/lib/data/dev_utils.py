import difflib
import random
from datetime import date, timedelta

from radar.lib.data.dev_constants import FIRST_NAMES, GENDER_FEMALE, GENDER_MALE, LAST_NAMES, ADDRESS_LINE_1, \
    ADDRESS_LINE_3, ADDRESS_LINE_2, POSTCODES
from radar.lib.utils import is_date, date_to_datetime


def generate_first_name_alias(gender, first_name):
    def f(x):
        if first_name == x:
            return 0
        else:
            return difflib.SequenceMatcher(None, first_name, x).ratio()

    return max(FIRST_NAMES[gender], key=f)


def generate_gender():
    if random.random() > 0.5:
        return GENDER_MALE
    else:
        return GENDER_FEMALE


def generate_first_name(gender):
    return random.choice(FIRST_NAMES[gender])


def generate_last_name():
    return random.choice(LAST_NAMES)


def generate_date_of_birth():
    return random_date(date(1920, 1, 1), date(2000, 12, 31))


def generate_date_of_death(date_of_birth):
    return random_date(date_of_birth, date(2014, 12, 31))


def random_date(start_date, end_date):
    if start_date == end_date:
        return start_date

    days = (end_date - start_date).days
    random_date = start_date + timedelta(days=random.randint(1, days))
    return random_date


def random_bool():
    return random.randint(0, 1) == 1


def random_datetime(start, end):
    if is_date(start):
        start_dt = date_to_datetime(start)
    else:
        start_dt = start

    if is_date(end):
        end_dt = date_to_datetime(end)
    else:
        end_dt = end

    seconds = int((end_dt - start_dt).total_seconds())
    return start_dt + timedelta(seconds=random.randrange(seconds))


def generate_email_address(first_name, last_name):
    return '%s.%s@example.org' % (first_name.lower(), last_name.lower())


def generate_phone_number():
    return '0%d%s %s' % (
        random.randint(1, 2),
        ''.join(str(random.randint(0, 9)) for _ in range(3)),
        ''.join(str(random.randint(0, 9)) for _ in range(6)),
    )


def generate_mobile_number():
    return '07' + ''.join(str(random.randint(0, 9)) for _ in range(9))


def generate_nhs_no():
    while True:
        number = ''.join(str(random.randint(0, 9)) for _ in range(9))

        check_digit = 0

        for i in range(9):
            check_digit += int(number[i]) * (10 - i)

        check_digit = 11 - (check_digit % 11)

        if check_digit == 11:
            check_digit = 0
        elif check_digit == 10:
            continue

        number += str(check_digit)

        return number


def generate_chi_no():
    return generate_nhs_no()


def generate_ukrr_no():
    return str(random.randint(199900001, 201599999))


def generate_nhsbt_no():
    return str(random.randint(1, 200000))


def generate_address_line_1():
    return random.choice(ADDRESS_LINE_1)


def generate_address_line_2():
    return random.choice(ADDRESS_LINE_2)


def generate_address_line_3():
    return random.choice(ADDRESS_LINE_3)


def generate_postcode():
    return random.choice(POSTCODES)
