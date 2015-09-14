from radar.lib.serializers import IntegerField


def test_int():
    assert to_data(123) == 123


def test_none():
    assert to_data(None) is None


def to_data(value):
    field = IntegerField()
    field.bind('test')
    value = field.get_value({'test': value})
    data = field.to_data(value)
    return data
