from radar.lib.validation.validators import none_if_blank


def test_blank():
    assert none_if_blank()('') is None


def test_not_blank():
    assert none_if_blank()('hello') == 'hello'
