import pytest
from radar.lib.validation.core import ValidationError
from radar.lib.validation.validators import not_empty


def test_str():
    value = not_empty()('hello')
    assert value == 'hello'


def test_list():
    value = not_empty()(['hello', 'world'])
    assert value == ['hello', 'world']


def test_empty_str():
    with pytest.raises(ValidationError):
        not_empty()('')


def test_empty_list():
    with pytest.raises(ValidationError):
        not_empty()([])
