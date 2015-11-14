from radar.validation.validators import default


def test_none():
    assert default('Hello')(None) == 'Hello'


def test_not_none():
    assert default('Hello')('World') == 'World'


def test_function():
    assert default(lambda: 'Hello')(None) == 'Hello'
