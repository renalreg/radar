import pytest
from radar.validation.core import ValidationError
from radar.validation.validators import in_


def test_in_list():
    value = in_([1, 2, 3])(1)
    assert value == 1


def test_not_in_list():
    with pytest.raises(ValidationError):
        in_([1, 2, 3])(4)
