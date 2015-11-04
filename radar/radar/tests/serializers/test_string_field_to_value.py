import pytest

from radar.serializers.fields import StringField
from radar.validation.core import ValidationError


def test_string():
    assert to_value('hello') == 'hello'


def test_unicode():
    # Smiley face
    assert to_value(u'\u263A') == u'\u263A'


def test_int():
    assert to_value(123) == '123'


def test_decimal():
    assert to_value(123.456) == '123.456'


def test_null():
    assert to_value(None) is None


def test_strip():
    assert to_value(' foo ') == 'foo'


def test_true():
    to_value_invalid(True)


def test_false():
    to_value_invalid(False)


def test_object():
    to_value_invalid({'foo': 1, 'bar': 2})


def test_list():
    to_value_invalid(['foo', 'bar', 'baz'])


def to_value_invalid(data):
    with pytest.raises(ValidationError):
        to_value(data)


def to_value(data):
    field = StringField()
    field.bind('test')
    data = field.get_data({'test': data})
    value = field.to_value(data)
    return value
