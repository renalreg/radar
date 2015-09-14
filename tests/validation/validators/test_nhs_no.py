import pytest

from radar.lib.validation.core import ValidationError
from radar.lib.validation.validators import nhs_no


def test_valid():
    # https://en.wikipedia.org/wiki/NHS_number
    assert valid(9434765919) == 9434765919
    assert valid(9434765870) == 9434765870


def test_invalid():
    invalid(9434765918)
    invalid(9434765871)


def valid(value):
    return nhs_no()(value)


def invalid(value):
    with pytest.raises(ValidationError) as e:
        nhs_no()(value)

    return e
