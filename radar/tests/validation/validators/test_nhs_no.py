import pytest

from radar.validation.core import ValidationError
from radar.validation.patient_number_validators import nhs_no


def test_valid_int():
    # https://en.wikipedia.org/wiki/NHS_number
    assert valid(9434765919) == 9434765919
    assert valid(9434765870) == 9434765870


def test_valid_string():
    assert valid('9434765919') == '9434765919'
    assert valid('9434765870') == '9434765870'


def test_short_string():
    assert valid('437631966') == '437631966'


def test_short_int():
    assert valid(437631966) == 437631966


def test_invalid():
    invalid(9434765918)
    invalid(9434765871)


def test_invalid_string():
    invalid('9434765918')
    invalid('9434765871')


def test_remove_spaces():
    value = valid('943 476 5919')
    assert value == '9434765919'


def test_remove_leading_zeros():
    value = valid('0009434765919')
    assert value == '9434765919'


def valid(value):
    return nhs_no()(value)


def invalid(value):
    with pytest.raises(ValidationError) as e:
        nhs_no()(value)

    return e
