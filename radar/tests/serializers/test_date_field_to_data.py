from datetime import date

from radar.lib.serializers.fields import DateField


def test_date():
    assert to_data(date(2001, 2, 3)) == '2001-02-03'


def test_old_date():
    assert to_data(date(999, 1, 1)) == '0999-01-01'


def test_none():
    assert to_data(None) is None


def to_data(value):
    field = DateField()
    field.bind('test')
    value = field.get_value({'test': value})
    data = field.to_data(value)
    return data
