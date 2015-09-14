import pytest
from radar.lib.validation.core import ValidationError
from radar.lib.validation.validators import max_


def test_valid():
    value = max_(10)(5)
    assert value == 5


def test_less_than():
    max_(10)(9)


def test_equal():
    max_(10)(10)


def test_greater_than():
    with pytest.raises(ValidationError):
        max_(10)(11)
