from radar.utils import Enum


class FOO(Enum):
    FOO = 1
    FOO_BAR = 2
    FOO_BAR_BAZ = 3
    x = 4


def test_values():
    assert FOO.values() == [1, 2, 3]
