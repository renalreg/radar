from radar.web.template_filters import yn


def test_yn_true():
    assert yn(True) == 'Yes'


def test_yn_false():
    assert yn(False) == 'No'


def test_yn_empty():
    assert yn('') == ''


def test_yn_none():
    assert yn(None) == ''
