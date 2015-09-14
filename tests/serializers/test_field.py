from radar.lib.serializers import Field, Empty


class TestObj(object):
    def __init__(self, test=None):
        if test is not Empty:
            self.test = test


def test_get_value_dict():
    assert get_value({'test': 'foo'}) == 'foo'


def test_get_value_dict_missing():
    assert get_value({}) is Empty


def test_get_value_dict_none():
    assert get_value({'test': None}) is None


def test_get_value_obj():
    assert get_value(TestObj('foo')) == 'foo'


def test_get_value_obj_missing():
    assert get_value(TestObj(Empty)) is Empty


def test_get_value_obj_none():
    assert get_value(TestObj()) is None


def get_value(value):
    field = Field()
    field.bind('test')
    return field.get_value(value)


def test_get_data():
    assert get_data({'test': 'foo'}) == 'foo'


def test_get_data_none():
    assert get_data({'test': None}) is None


def test_get_data_missing():
    assert get_data({}) is Empty


def get_data(data):
    field = Field()
    field.bind('test')
    return field.get_data(data)


def get_transform_errors():
    assert transform_errors({'foo': 'hello'}) == {'bar': 'hello'}


def get_transform_errors_no_errors():
    assert transform_errors({'baz': 'hello'}) == {}


def get_transform_errors_direction():
    # source to field_name only
    assert transform_errors({'bar': 'hello'}) == {}


def transform_errors(errors):
    field = Field(source='foo')
    field.bind('bar')
    return field.get_data(errors)
