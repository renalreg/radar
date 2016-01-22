from enum import Enum

from radar.serializers.fields import EnumField


class Foo(Enum):
    a = 'foo'
    b = 'bar'
    c = 'baz'

    def __str__(self):
        return str(self.value)


def test_none():
    assert to_data(None) is None


def test_enum():
    assert to_data(Foo.a) == 'foo'


def test_str():
    assert to_data('foo') == 'foo'


def to_data(value):
    field = EnumField(Foo)
    field.bind('test')
    value = field.get_value({'test': value})
    data = field.to_data(value)
    return data
