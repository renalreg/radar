import pytest
from radar.lib.validation.core import ValidationError
from radar.lib.validation.validators import postcode


def test_valid():
    value = valid('BS10 5NB')
    assert value == 'BS10 5NB'


def test_remove_spaces():
    value = valid('BS10   5NB')
    assert value == 'BS10 5NB'


def test_add_space():
    value = valid('BS105NB')
    assert value == 'BS10 5NB'


def test_bfpo_add_space():
    value = valid('BFPO1234')
    assert value == 'BFPO 1234'


def test_to_upper():
    value = valid('bs10 5nb')
    assert value == 'BS10 5NB'


def test_blank():
    invalid('')


def test_prefix_junk():
    invalid('JUNKBS10 5NB')


def test_suffix_junk():
    invalid('BS10 5NBJUNK')


def test_invalid():
    invalid('HELLO')


def valid(value):
    return postcode()(value)


def invalid(value):
    with pytest.raises(ValidationError) as e:
        postcode()(value)

    return e
