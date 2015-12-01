import pytest

from radar.utils import seconds_to_age


@pytest.mark.parametrize(['seconds', 'expected'], [
    (0, 0),  # 0 seconds => 0 months
    (86400, 0),  # 1 day => 0 months
    (2628000, 2628000),  # 42 days => 1 month
    (34560000, 34164000),  # 400 days => 1 year, 1 month
    (165564000, 157680000),  # 5 years, 3 months => 5 years
])
def test(seconds, expected):
    assert seconds_to_age(seconds) == expected
