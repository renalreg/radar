import pytest

from radar.validation.core import ValidationError
from radar.validation.number_validators import chi_no


def test_valid_int():
    assert valid(101299877) == 101299877


def test_valid_string():
    assert valid('101299877') == '0101299877'


def test_short_string():
    assert valid('437631966') == '0437631966'


def test_short_int():
    assert valid(437631966) == 437631966


def test_nhs_no():
    invalid('9434765919')


def test_handc_no():
    invalid('3232255825')


def valid(value):
    return chi_no()(value)


def invalid(value):
    with pytest.raises(ValidationError) as e:
        chi_no()(value)

    return e
