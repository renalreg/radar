from datetime import date

from radar.serializers.fields import DateField, ListField


def test_list():
    assert to_data([date(2000, 1, 1), date(2000, 1, 2), date(2000, 1, 3)]) == ['2000-01-01', '2000-01-02', '2000-01-03']


def test_empty_list():
    assert to_data([]) == []


def test_none():
    assert to_data(None) is None


def to_data(value):
    field = ListField(DateField())
    field.bind('test')
    value = field.get_value({'test': value})
    data = field.to_data(value)
    return data
