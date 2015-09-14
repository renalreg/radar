import pytest
from radar.lib.validation.core import ValidationError
from radar.lib.validation.validators import required


def test_str():
    required()('hello')


def test_int():
    required()(123)


def test_empty():
    required()('')


def test_none():
    with pytest.raises(ValidationError):
        required()(None)
