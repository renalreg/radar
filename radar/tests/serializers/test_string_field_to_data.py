from radar.lib.serializers.fields import StringField


def test_string():
    assert to_data('hello') == 'hello'


def test_unicode():
    # Smiley face
    assert to_data(u'\u263A') == u'\u263A'


def test_none():
    assert to_data(None) is None


def to_data(value):
    field = StringField()
    field.bind('test')
    value = field.get_value({'test': value})
    data = field.to_data(value)
    return data
