from datetime import date, datetime

from radar.web.template_filters import yn, missing, year_format, date_format, datetime_format, strftime


def test_yn_true():
    assert yn(True) == 'Yes'


def test_yn_false():
    assert yn(False) == 'No'


def test_yn_none():
    assert yn(None) == '-'


def test_missing_not_missing():
    assert missing('hello') == 'hello'


def test_missing_empty():
    assert missing('') == '-'


def test_missing_none():
    assert missing(None) == '-'


def test_year_format_999():
    assert year_format(date(999, 1, 1)) == '0999'


def test_year_format_1800():
    assert year_format(date(1800, 1, 1)) == '1800'


def test_year_format_date():
    assert year_format(date(2015, 1, 1)) == '2015'


def test_year_format_datetime():
    assert year_format(datetime(2015, 1, 1)) == '2015'


def test_date_format_999():
    assert date_format(date(999, 1, 2)) == '02/01/0999'


def test_date_format_1800():
    assert date_format(date(1800, 1, 2)) == '02/01/1800'


def test_date_format_date():
    assert date_format(date(2015, 1, 2)) == '02/01/2015'


def test_date_format_datetime():
    assert date_format(datetime(2015, 1, 2)) == '02/01/2015'


def test_datetime_format_datetime():
    assert datetime_format(datetime(2015, 1, 2, 3, 4)) == '02/01/2015 03:04'


def test_datetime_format_datetime_seconds():
    assert datetime_format(datetime(2015, 1, 2, 3, 4, 5), seconds=True) == '02/01/2015 03:04:05'


def test_datetime_format_date():
    assert datetime_format(date(2015, 1, 2)) == '02/01/2015 00:00'


def test_datetime_format_date_seconds():
    assert datetime_format(date(2015, 1, 2), seconds=True) == '02/01/2015 00:00:00'


def test_datetime_format_999():
    assert datetime_format(datetime(999, 1, 2, 3, 4)) == '02/01/0999 03:04'


def test_datetime_format_1800():
    assert datetime_format(datetime(1800, 1, 2, 3, 4)) == '02/01/1800 03:04'


def test_strftime_none():
    assert strftime(None, '%Y-%m-%d') == ''


def test_strftime_date():
    assert strftime(date(2015, 1, 2), '%Y-%m-%d') == '2015-01-02'


def test_strftime_datetime():
    assert strftime(datetime(2015, 1, 2, 3, 4, 5), '%Y-%m-%d %H:%M:%S') == '2015-01-02 03:04:05'
