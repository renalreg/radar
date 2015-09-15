from datetime import datetime
import pytest

import pytz

from radar.lib.safe_strftime import safe_strftime


SAFE_STRFTIME_DIRECTIVES = {
    'Y': lambda x: '%04d' % x.year,
    'y': lambda x: ('%04d' % x.year)[-2:],
    'm': lambda x: '%02d' % x.month,
    'd': lambda x: '%02d' % x.day,
    'H': lambda x: '%02d' % x.hour,
    'I': lambda x: '%02d' % (x.hour % 12),
    'M': lambda x: '%02d' % x.minute,
    'S': lambda x: '%02d' % x.second,
}


def test_iso_format():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), '%Y-%m-%dT%H:%M:%SZ') == '1234-01-02T03:04:05Z'


def test_yyyymmdd():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), '%Y-%m-%d') == '1234-01-02'


def test_ddmmyyyy():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), '%d/%m/%Y') == '02/01/1234'


def test_y_upper():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), '%Y') == '1234'


def test_y_lower():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), '%y') == '34'


def test_m_lower():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), '%m') == '01'


def test_d_lower():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), '%d') == '02'


def test_h_upper_am():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), '%H') == '03'


def test_h_upper_pm():
    assert safe_strftime(datetime(1234, 1, 2, 15, 4, 5, tzinfo=pytz.UTC), '%H') == '15'


def test_i_upper_am():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), '%I') == '03'


def test_i_upper_pm():
    assert safe_strftime(datetime(1234, 1, 2, 15, 4, 5, tzinfo=pytz.UTC), '%I') == '03'


def test_m_upper():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), '%M') == '04'


def test_s_upper():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), '%S') == '05'


def test_percent():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), '100%%') == '100%'


def test_invalid_directive():
    with pytest.raises(ValueError) as e:
        safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), '%e')

    assert e.value.message == 'Invalid format string'


def test_blank():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), '') == ''
