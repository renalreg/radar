import pytest

from radar.validation.core import ValidationError
from radar.validation.validators import no_trailing_slash


def test_valid():
    assert valid('foo') == 'foo'
    assert valid('foo/bar') == 'foo/bar'


def test_trailing_slash():
    invalid('foo/')


def valid(value):
    return no_trailing_slash()(value)


def invalid(value):
    with pytest.raises(ValidationError) as e:
        no_trailing_slash()(value)

    return e
