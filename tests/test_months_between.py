from datetime import datetime

import pytest

from radar.utils import months_between


@pytest.mark.parametrize(['a', 'b', 'expected'], [
    (datetime(2017, 1, 1), datetime(2016, 12, 31), 0),
    (datetime(2017, 2, 9), datetime(2017, 1, 10), 0),
    (datetime(2017, 2, 10), datetime(2017, 1, 10), 1),
    (datetime(2017, 2, 11), datetime(2017, 1, 10), 1),
    (datetime(2020, 1, 1), datetime(2017, 1, 1), 36),
])
def test(a, b, expected):
    assert months_between(a, b) == expected
