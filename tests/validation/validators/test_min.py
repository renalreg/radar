import pytest
from radar.lib.validation.core import ValidationError
from radar.lib.validation.validators import min_


def test_less_than():
    with pytest.raises(ValidationError):
        min_(10)(9)


def test_equal():
    min_(10)(10)


def test_greater_than():
    min_(10)(11)
