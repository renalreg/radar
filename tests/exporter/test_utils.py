import pytest

from radar.exporter.exporters import (
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
