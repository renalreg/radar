from enum import Enum

from radar.serializers.fields import EnumField


class Foo(Enum):
    a = 'foo'
    b = 'bar'
    c = 'baz'


def test_none():
    assert to_data(None) is None


def test_enum():
    assert to_data(Foo.a) == 'foo'


def test_str():
    assert to_data('foo') == 'foo'


def to_data(value):
    field = EnumField()
    field.bind('test')
    value = field.get_value({'test': value})
    data = field.to_data(value)
    return data
