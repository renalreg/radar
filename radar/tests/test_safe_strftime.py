from datetime import datetime
import pytest

import pytz

from radar.lib.safe_strftime import safe_strftime


def test_iso_format():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.utc), '%Y-%m-%dT%H:%M:%SZ') == '1234-01-02T03:04:05Z'


def test_yyyymmdd():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.utc), '%Y-%m-%d') == '1234-01-02'


def test_ddmmyyyy():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.utc), '%d/%m/%Y') == '02/01/1234'


def test_y_upper():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.utc), '%Y') == '1234'


def test_y_lower():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.utc), '%y') == '34'


def test_b_upper():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.utc), '%B') == 'January'
    assert safe_strftime(datetime(1234, 2, 2, 3, 4, 5, tzinfo=pytz.utc), '%B') == 'February'
    assert safe_strftime(datetime(1234, 3, 2, 3, 4, 5, tzinfo=pytz.utc), '%B') == 'March'
    assert safe_strftime(datetime(1234, 4, 2, 3, 4, 5, tzinfo=pytz.utc), '%B') == 'April'
    assert safe_strftime(datetime(1234, 5, 2, 3, 4, 5, tzinfo=pytz.utc), '%B') == 'May'
    assert safe_strftime(datetime(1234, 6, 2, 3, 4, 5, tzinfo=pytz.utc), '%B') == 'June'
    assert safe_strftime(datetime(1234, 7, 2, 3, 4, 5, tzinfo=pytz.utc), '%B') == 'July'
    assert safe_strftime(datetime(1234, 8, 2, 3, 4, 5, tzinfo=pytz.utc), '%B') == 'August'
    assert safe_strftime(datetime(1234, 9, 2, 3, 4, 5, tzinfo=pytz.utc), '%B') == 'September'
    assert safe_strftime(datetime(1234, 10, 2, 3, 4, 5, tzinfo=pytz.utc), '%B') == 'October'
    assert safe_strftime(datetime(1234, 11, 2, 3, 4, 5, tzinfo=pytz.utc), '%B') == 'November'
    assert safe_strftime(datetime(1234, 12, 2, 3, 4, 5, tzinfo=pytz.utc), '%B') == 'December'


def test_b_lower():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.utc), '%b') == 'Jan'
    assert safe_strftime(datetime(1234, 2, 2, 3, 4, 5, tzinfo=pytz.utc), '%b') == 'Feb'
    assert safe_strftime(datetime(1234, 3, 2, 3, 4, 5, tzinfo=pytz.utc), '%b') == 'Mar'
    assert safe_strftime(datetime(1234, 4, 2, 3, 4, 5, tzinfo=pytz.utc), '%b') == 'Apr'
    assert safe_strftime(datetime(1234, 5, 2, 3, 4, 5, tzinfo=pytz.utc), '%b') == 'May'
    assert safe_strftime(datetime(1234, 6, 2, 3, 4, 5, tzinfo=pytz.utc), '%b') == 'Jun'
    assert safe_strftime(datetime(1234, 7, 2, 3, 4, 5, tzinfo=pytz.utc), '%b') == 'Jul'
    assert safe_strftime(datetime(1234, 8, 2, 3, 4, 5, tzinfo=pytz.utc), '%b') == 'Aug'
    assert safe_strftime(datetime(1234, 9, 2, 3, 4, 5, tzinfo=pytz.utc), '%b') == 'Sep'
    assert safe_strftime(datetime(1234, 10, 2, 3, 4, 5, tzinfo=pytz.utc), '%b') == 'Oct'
    assert safe_strftime(datetime(1234, 11, 2, 3, 4, 5, tzinfo=pytz.utc), '%b') == 'Nov'
    assert safe_strftime(datetime(1234, 12, 2, 3, 4, 5, tzinfo=pytz.utc), '%b') == 'Dec'


def test_m_lower():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.utc), '%m') == '01'


def test_d_lower():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.utc), '%d') == '02'


def test_h_upper_am():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.utc), '%H') == '03'


def test_h_upper_pm():
    assert safe_strftime(datetime(1234, 1, 2, 15, 4, 5, tzinfo=pytz.utc), '%H') == '15'


def test_i_upper_am():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.utc), '%I') == '03'


def test_i_upper_pm():
    assert safe_strftime(datetime(1234, 1, 2, 15, 4, 5, tzinfo=pytz.utc), '%I') == '03'


def test_p_lower():
    assert safe_strftime(datetime(1234, 1, 2, 0, 0, 0, tzinfo=pytz.utc), '%p') == 'AM'
    assert safe_strftime(datetime(1234, 1, 2, 11, 0, 0, tzinfo=pytz.utc), '%p') == 'AM'
    assert safe_strftime(datetime(1234, 1, 2, 12, 0, 0, tzinfo=pytz.utc), '%p') == 'PM'
    assert safe_strftime(datetime(1234, 1, 2, 13, 0, 0, tzinfo=pytz.utc), '%p') == 'PM'
    assert safe_strftime(datetime(1234, 1, 2, 23, 0, 0, tzinfo=pytz.utc), '%p') == 'PM'


def test_m_upper():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.utc), '%M') == '04'


def test_s_upper():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.utc), '%S') == '05'


def test_f_lower():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, 123, tzinfo=pytz.utc), '%f') == '000123'


def test_percent():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.utc), '100%%') == '100%'


def test_invalid_directive():
    with pytest.raises(ValueError) as e:
        safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.utc), '%e')

    assert e.value.message == 'Invalid format string'


def test_blank():
    assert safe_strftime(datetime(1234, 1, 2, 3, 4, 5, tzinfo=pytz.utc), '') == ''
