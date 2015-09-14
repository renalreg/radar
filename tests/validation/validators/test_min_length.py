import pytest
from radar.lib.validation.core import ValidationError
from radar.lib.validation.validators import min_length


def test_valid():
    value = min_length(3)('abc')
    assert value == 'abc'


def test_empty():
    with pytest.raises(ValidationError):
        min_length(3)('')


def test_shorter():
    with pytest.raises(ValidationError):
        min_length(3)('aa')


def test_equal():
    min_length(3)('aaa')


def test_longer():
    min_length(3)('aaaa')
