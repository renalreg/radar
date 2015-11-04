from radar.validation.validators import upper


def test_lower():
    assert upper()('foo bar') == 'FOO BAR'


def test_upper():
    assert upper()('FOO BAR') == 'FOO BAR'


def test_blank():
    assert upper()('') == ''
