from radar.validation.validators import normalise_whitespace


def test_no_spaces():
    value = normalise_whitespace()('foo')
    assert value == 'foo'


def test_single_space():
    value = normalise_whitespace()('foo bar baz')
    assert value == 'foo bar baz'


def test_multiple_spaces():
    value = normalise_whitespace()('foo   bar   baz')
    assert value == 'foo bar baz'


def test_single_tab():
    value = normalise_whitespace()('foo\tbar\tbaz')
    assert value == 'foo bar baz'


def test_multiple_tabs():
    value = normalise_whitespace()('foo\t\t\tbar\t\t\tbaz')
    assert value == 'foo bar baz'
