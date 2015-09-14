from radar.lib.serializers import BooleanField


def test_true():
    assert to_data(True) is True


def test_false():
    assert to_data(False) is False


def test_1():
    assert to_data(1) is True


def test_0():
    assert to_data(0) is False


def test_none():
    assert to_data(None) is None


def to_data(value):
    field = BooleanField()
    field.bind('test')
    value = field.get_value({'test': value})
    data = field.to_data(value)
    return data
