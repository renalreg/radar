from radar.lib.validation.validators import remove_trailing_comma


def test_no_comma():
    value = remove_trailing_comma()('foo')
    assert value == 'foo'


def test_no_comma_with_spaces():
    value = remove_trailing_comma()('foo   ')
    assert value == 'foo   '


def test_comma():
    value = remove_trailing_comma()('foo,')
    assert value == 'foo'


def test_comma_with_spaces():
    value = remove_trailing_comma()('foo   ,')
    assert value == 'foo'


def test_blank():
    value = remove_trailing_comma()('')
    assert value == ''


def test_just_comma():
    value = remove_trailing_comma()(',')
    assert value == ''
