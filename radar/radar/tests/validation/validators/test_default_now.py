from datetime import datetime

from freezegun import freeze_time
import pytz

from radar.validation.validators import default_now as _default_now

default_now = _default_now()

NOW = datetime(2000, 1, 2, 3, 4, 5)


@freeze_time("2000-01-01")
def test_none():
    assert default_now(None) == datetime(2000, 1, 1, tzinfo=pytz.UTC)


def test_not_none():
    x = datetime(2015, 1, 2, 3, 4, 5)
    assert default_now(x) == x
