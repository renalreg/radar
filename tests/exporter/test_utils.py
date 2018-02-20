from datetime import datetime

import pytest

from radar.exporter.exporters import (
    format_date,
    get_months,
    get_years,
    identity_getter,
    none_getter,
    path_getter
)


class C(object):
    pass


@pytest.mark.parametrize(['months', 'expected'], [
    (6, 6),
    (12, 0),
    (18, 6),
])
def test_get_months(months, expected):
    assert get_months(months) == expected


@pytest.mark.parametrize(['months', 'expected'], [
    (6, 0),
    (12, 1),
    (18, 1),
])
def test_get_years(months, expected):
    assert get_years(months) == expected


def test_path_getter():
    a = C()
    a.b = C()
    a.b.c = C()

    f = path_getter('b.c')

    assert f(a) is a.b.c

    a.b = None

    assert f(a) is None


def test_identity_getter():
    c = C()
    assert identity_getter(c) is c


def test_none_getter():
    assert none_getter(123) is None


def test_format_date_correctly_behaves_on_normal_input():
    dt = datetime(2018, 1, 1, 14, 35, 32)
    expected = '01/01/2018'
    assert format_date(dt) == expected


def test_format_date_correctly_returns_on_year_before_1900():
    dt = datetime(1895, 1, 1, 14, 35, 32)
    expected = '01/01/1895'
    assert format_date(dt) == expected


def test_format_date_correctly_behaves_on_given_string_date():
    dt = '2018-01-01'
    assert format_date(dt) == '01/01/2018'


def test_format_date_correctly_behaves_on_given_string_date_before_1900():
    dt = '1895-01-01'
    assert format_date(dt) == '01/01/1895'


def test_format_date_returns_unmodified_on_non_date():
    inp = 'anything'
    assert format_date(inp) == inp
