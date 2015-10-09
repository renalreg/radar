import pytest
from radar.validation.core import ValidatorCall, ValidationError
from radar.validation.validators import range_


def test_valid():
    call = ValidatorCall({}, 0)
    value = call(range_(min_value=3, max_value=5), 4)
    assert value == 4


def test_min_less_than():
    call = ValidatorCall({}, 0)

    with pytest.raises(ValidationError):
        call(range_(min_value=10), 9)


def test_min_equal():
    call = ValidatorCall({}, 0)
    call(range_(min_value=10), 10)


def test_min_greater_than():
    call = ValidatorCall({}, 0)
    call(range_(min_value=10), 11)


def test_max_less_than():
    call = ValidatorCall({}, 0)
    call(range_(max_value=10), 9)


def test_max_equal():
    call = ValidatorCall({}, 0)
    call(range_(max_value=10), 10)


def test_max_greater_than():
    call = ValidatorCall({}, 0)

    with pytest.raises(ValidationError):
        call(range_(max_value=10), 11)


def test_min_max_less_than():
    call = ValidatorCall({}, 0)

    with pytest.raises(ValidationError):
        call(range_(10, 20), 5)


def test_min_max_equal_min():
    call = ValidatorCall({}, 0)
    call(range_(10, 20), 10)


def test_min_max_middle():
    call = ValidatorCall({}, 0)
    call(range_(10, 20), 15)


def test_min_max_equal_max():
    call = ValidatorCall({}, 0)
    call(range_(10, 20), 20)


def test_min_max_greater_than():
    call = ValidatorCall({}, 0)

    with pytest.raises(ValidationError):
        call(range_(10, 20), 21)
