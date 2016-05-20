import pytest
from cornflake.exceptions import ValidationError

from radar.api.serializers.validators import ukrdc_no


def test_invalid_string():
    invalid('hello')


def test_valid_int():
    assert valid(100000123) == 100000123


def test_valid_string():
    assert valid('100000123') == '100000123'


def test_remove_spaces():
    assert valid('100 000 123') == '100000123'


def test_remove_leading_zeros():
    assert valid('000100000123') == '100000123'


def test_less_than_lower_limit_int():
    invalid(100000000)


def test_less_than_lower_limit_string():
    invalid('100000000')


def test_equal_to_lower_limit_int():
    assert valid(100000001) == 100000001


def test_equal_to_lower_limit_string():
    assert valid('100000001') == '100000001'


def test_equal_to_upper_limit_int():
    assert valid(999999999) == 999999999


def test_equal_to_upper_limit_string():
    assert valid('999999999') == '999999999'


def test_greater_than_upper_limit_int():
    invalid(1000000000)


def test_greater_than_upper_limit_string():
    invalid('1000000000')


def valid(value):
    return ukrdc_no()(value)


def invalid(value):
    with pytest.raises(ValidationError) as e:
        ukrdc_no()(value)

    return e
