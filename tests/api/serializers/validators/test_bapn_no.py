from cornflake.exceptions import ValidationError
import pytest

from radar.api.serializers.validators import bapn_no


def test_valid():
    assert valid('A1') == 'A1'
    assert valid('G26') == 'G26'
    assert valid('N310') == 'N310'


def test_remove_leading_zeros():
    valid('A001') == 'A1'
    valid('A01') == 'A1'


def test_too_many_leading_zeros():
    invalid('A0001')


def test_invalid_letter():
    invalid('Z123')


def test_too_many_digits():
    invalid('A1234')


def test_junk_prefix():
    invalid('JUNKA123')


def test_junk_suffix():
    invalid('A123JUNK')


def valid(value):
    return bapn_no()(value)


def invalid(value):
    with pytest.raises(ValidationError) as e:
        bapn_no()(value)

    return e
