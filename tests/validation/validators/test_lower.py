from radar.lib.validation.validators import lower


def test_lower():
    assert lower()('foo bar') == 'foo bar'


def test_upper():
    assert lower()('FOO BAR') == 'foo bar'


def test_blank():
    assert lower()('') == ''
