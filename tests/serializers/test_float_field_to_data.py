from decimal import Decimal
from radar.lib.serializers import FloatField


def test_int():
    assert to_data(123) == 123


def test_float():
    assert to_data(123.456) == 123.456


def test_decimal():
    assert to_data(Decimal(123.456)) == 123.456


def test_none():
    assert to_data(None) is None


def to_data(value):
    field = FloatField()
    field.bind('test')
    value = field.get_value({'test': value})
    data = field.to_data(value)
    return data
