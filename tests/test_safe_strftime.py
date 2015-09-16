from datetime import datetime
import pytest

import pytz

from radar.lib.safe_strftime import safe_strftime


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


def test_b_upper():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), '%B') == 'January'
    assert safe_strftime(datetime(1234, 2, 2, 3, 4, 5, tzinfo=pytz.UTC), '%B') == 'February'
    assert safe_strftime(datetime(1234, 3, 2, 3, 4, 5, tzinfo=pytz.UTC), '%B') == 'March'
    assert safe_strftime(datetime(1234, 4, 2, 3, 4, 5, tzinfo=pytz.UTC), '%B') == 'April'
    assert safe_strftime(datetime(1234, 5, 2, 3, 4, 5, tzinfo=pytz.UTC), '%B') == 'May'
    assert safe_strftime(datetime(1234, 6, 2, 3, 4, 5, tzinfo=pytz.UTC), '%B') == 'June'
    assert safe_strftime(datetime(1234, 7, 2, 3, 4, 5, tzinfo=pytz.UTC), '%B') == 'July'
    assert safe_strftime(datetime(1234, 8, 2, 3, 4, 5, tzinfo=pytz.UTC), '%B') == 'August'
    assert safe_strftime(datetime(1234, 9, 2, 3, 4, 5, tzinfo=pytz.UTC), '%B') == 'September'
    assert safe_strftime(datetime(1234, 10, 2, 3, 4, 5, tzinfo=pytz.UTC), '%B') == 'October'
    assert safe_strftime(datetime(1234, 11, 2, 3, 4, 5, tzinfo=pytz.UTC), '%B') == 'November'
    assert safe_strftime(datetime(1234, 12, 2, 3, 4, 5, tzinfo=pytz.UTC), '%B') == 'December'


def test_b_lower():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), '%b') == 'Jan'
    assert safe_strftime(datetime(1234, 2, 2, 3, 4, 5, tzinfo=pytz.UTC), '%b') == 'Feb'
    assert safe_strftime(datetime(1234, 3, 2, 3, 4, 5, tzinfo=pytz.UTC), '%b') == 'Mar'
    assert safe_strftime(datetime(1234, 4, 2, 3, 4, 5, tzinfo=pytz.UTC), '%b') == 'Apr'
    assert safe_strftime(datetime(1234, 5, 2, 3, 4, 5, tzinfo=pytz.UTC), '%b') == 'May'
    assert safe_strftime(datetime(1234, 6, 2, 3, 4, 5, tzinfo=pytz.UTC), '%b') == 'Jun'
    assert safe_strftime(datetime(1234, 7, 2, 3, 4, 5, tzinfo=pytz.UTC), '%b') == 'Jul'
    assert safe_strftime(datetime(1234, 8, 2, 3, 4, 5, tzinfo=pytz.UTC), '%b') == 'Aug'
    assert safe_strftime(datetime(1234, 9, 2, 3, 4, 5, tzinfo=pytz.UTC), '%b') == 'Sep'
    assert safe_strftime(datetime(1234, 10, 2, 3, 4, 5, tzinfo=pytz.UTC), '%b') == 'Oct'
    assert safe_strftime(datetime(1234, 11, 2, 3, 4, 5, tzinfo=pytz.UTC), '%b') == 'Nov'
    assert safe_strftime(datetime(1234, 12, 2, 3, 4, 5, tzinfo=pytz.UTC), '%b') == 'Dec'


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


def test_p_lower():
    assert safe_strftime(datetime(1234, 1, 2, 0, 0, 0, tzinfo=pytz.UTC), '%p') == 'AM'
    assert safe_strftime(datetime(1234, 1, 2, 11, 0, 0, tzinfo=pytz.UTC), '%p') == 'AM'
    assert safe_strftime(datetime(1234, 1, 2, 12, 0, 0, tzinfo=pytz.UTC), '%p') == 'PM'
    assert safe_strftime(datetime(1234, 1, 2, 13, 0, 0, tzinfo=pytz.UTC), '%p') == 'PM'
    assert safe_strftime(datetime(1234, 1, 2, 23, 0, 0, tzinfo=pytz.UTC), '%p') == 'PM'


def test_m_upper():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), '%M') == '04'


def test_s_upper():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), '%S') == '05'


def test_f_lower():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, 123, tzinfo=pytz.UTC), '%f') == '000123'


def test_percent():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), '100%%') == '100%'


def test_invalid_directive():
    with pytest.raises(ValueError) as e:
        safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), '%e')

    assert e.value.message == 'Invalid format string'


def test_blank():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.UTC), '') == ''
