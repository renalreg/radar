import pytest

from radar.utils import round_age


@pytest.mark.parametrize(['months', 'expected'], [
    (3, 3), # 3 months
    (60, 60), # 5 years
    (61, 60), # 5 years, 1 month
])
def test(months, expected):
    assert round_age(months) == expected
