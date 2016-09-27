from datetime import datetime, timedelta

import pytz

from radar.database import no_autoflush
from radar.models.groups import GroupPatient
from radar.ukrdc_exporter.group_selector import GroupSelector

A = 1
B = 2


@no_autoflush
def run(a_x, a_y, b_x, b_y):
    now = datetime(2000, 1, 1, tzinfo=pytz.UTC)

    membership_a = GroupPatient()
    membership_a.id = A
    membership_a.from_date = now + timedelta(days=a_x)

    membership_b = GroupPatient()
    membership_b.id = B
    membership_b.from_date = now + timedelta(days=b_x)

    if a_y is not None:
        membership_a.to_date = now + timedelta(days=a_y)

    if b_y is not None:
        membership_b.to_date = now + timedelta(days=b_y)

    selector = GroupSelector(now)
    result1 = selector.select_group(membership_a, membership_b)
    result2 = selector.select_group(membership_b, membership_a)

    # Test symmetry
    assert result1 is result2

    return result1.id


def test_past_current():
    assert run(-1, -1, 0, 0) == B


def test_past_future():
    assert run(-1, -1, 1, 1) == B


def test_current_future():
    assert run(0, 0, 1, 1) == A


def test_past_past():
    # Equal
    assert run(-1, -1, -1, -1) == B

    # From date
    assert run(-2, -1, -1, -1) == A

    # To date
    assert run(-2, -2, -2, -1) == B


def test_current_current():
    # Equal
    assert run(0, 0, 0, 0) == B

    # From date
    assert run(-1, None, 0, None) == A

    # To date
    assert run(0, None, 0, None) == B
    assert run(0, 0, 0, 1) == B
    assert run(0, 0, 0, None) == B


def test_future_future():
    # Equal
    assert run(1, 1, 1, 1) == B

    # From date
    assert run(1, None, 2, None) == A

    # To date
    assert run(1, None, 1, None) == B
    assert run(1, 1, 1, 2) == B
    assert run(1, 1, 1, None) == B
