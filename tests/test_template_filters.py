from datetime import date, datetime

from radar.lib.template_filters import safe_strftime_template_filter


def test_safe_strftime_1800():
    assert safe_strftime_template_filter(datetime(1800, 1, 2, 3, 4), '%Y-%m-%d') == '1800-01-02'


def test_safe_strftime_none():
    assert safe_strftime_template_filter(None, '%Y-%m-%d') == ''


def test_safe_strftime_date():
    assert safe_strftime_template_filter(date(2015, 1, 2), '%Y-%m-%d') == '2015-01-02'


def test_safe_strftime_datetime():
    assert safe_strftime_template_filter(datetime(2015, 1, 2, 3, 4, 5), '%Y-%m-%d %H:%M:%S') == '2015-01-02 03:04:05'
