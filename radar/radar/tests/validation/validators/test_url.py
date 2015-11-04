import pytest

from radar.validation.core import ValidationError
from radar.validation.validators import url


def test_valid():
    assert valid('http://localhost/foo/bar.html') == 'http://localhost/foo/bar.html'
    assert valid('https://localhost') == 'https://localhost'
    assert valid('http://127.0.0.1') == 'http://127.0.0.1'


def test_no_network_location():
    invalid('http:///foo/bar/baz.html')


def test_no_schema():
    invalid('/foo/bar/baz.html')


def valid(value):
    return url()(value)


def invalid(value):
    with pytest.raises(ValidationError) as e:
        url()(value)

    return e
