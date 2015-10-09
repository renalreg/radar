from radar.lib.serializers.core import Empty
from test_serializer import FooSerializer, FooModel


def test_obj():
    assert to_data(FooModel(1, 2)) == {'foo': 1, 'bar': 2}


def test_obj_missing():
    assert to_data(FooModel(Empty, 2)) == {'bar': 2}


def test_obj_none():
    assert to_data(FooModel(None, 2)) == {'foo': None, 'bar': 2}


def test_dict():
    assert to_data({'foo': 1, 'bar': 2}) == {'foo': 1, 'bar': 2}


def test_dict_missing():
    assert to_data({'bar': 2}) == {'bar': 2}


def test_dict_none():
    assert to_data({'foo': None, 'bar': 2}) == {'foo': None, 'bar': 2}


def test_none():
    assert to_data(None) is None


def to_data(value):
    field = FooSerializer()
    field.bind('test')
    value = field.get_value({'test': value})
    data = field.to_data(value)
    return data
