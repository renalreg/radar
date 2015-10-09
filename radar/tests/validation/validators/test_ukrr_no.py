import pytest
from radar.validation.core import ValidationError
from radar.validation.patient_number_validators import ukrr_no


def test_valid_int():
    value = ukrr_no()(200012345)
    assert value == 200012345


def test_valid_string():
    value = ukrr_no()('200012345')
    assert value == '200012345'


def test_remove_slash():
    value = ukrr_no()('2000/12345')
    assert value == '200012345'


def test_remove_spaces():
    value = ukrr_no()('2000 12345')
    assert value == '200012345'


def test_remove_leading_zeros():
    value = ukrr_no()('000200012345')
    assert value == '200012345'


def test_less_than_lower_limit_int():
    with pytest.raises(ValidationError):
        ukrr_no()(199600000)


def test_less_than_lower_limit_string():
    with pytest.raises(ValidationError):
        ukrr_no()('199600000')


def test_equal_to_lower_limit_int():
    with pytest.raises(ValidationError):
        ukrr_no()(199600000)


def test_equal_to_lower_limit_string():
    with pytest.raises(ValidationError):
        ukrr_no()('199600000')


def test_equal_to_upper_limit_int():
    value = ukrr_no()(999999999)
    assert value == 999999999


def test_equal_to_upper_limit_string():
    value = ukrr_no()('999999999')
    assert value == '999999999'


def test_greater_than_upper_limit_int():
    with pytest.raises(ValidationError):
        ukrr_no()(1000000000)


def test_greater_than_upper_limit_string():
    with pytest.raises(ValidationError):
        ukrr_no()('1000000000')
