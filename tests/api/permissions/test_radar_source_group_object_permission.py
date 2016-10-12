import pytest

from radar.api.permissions import RadarSourceObjectPermission
from radar.models.groups import Group, GROUP_TYPE, GROUP_CODE_RADAR
from radar.models.medications import Medication
from radar.models.source_types import SOURCE_TYPE_RADAR, SOURCE_TYPE_UKRDC
from tests.api.permissions.helpers import MockRequest
from tests.permissions.helpers import make_user
from radar.roles import ROLE


READ = 0
WRITE = 1

DENY = False
GRANT = True

NOT_ADMIN = False
ADMIN = True


def make_request(action):
    if action == READ:
        method = 'GET'
    else:
        method = 'POST'

    return MockRequest(method)


def make_obj(source_type):
    if source_type == SOURCE_TYPE_RADAR:
        source_group = Group(code=GROUP_CODE_RADAR, type=GROUP_TYPE.SYSTEM)
    else:
        source_group = Group(code='REE01', type=GROUP_TYPE.HOSPITAL)

    obj = Medication()
    obj.source_group = source_group
    obj.source_type = source_type

    return obj


@pytest.mark.parametrize(['is_admin', 'action', 'source_type', 'expected'], [
    (NOT_ADMIN, READ, SOURCE_TYPE_RADAR, GRANT),
    (NOT_ADMIN, READ, SOURCE_TYPE_UKRDC, GRANT),
    (NOT_ADMIN, WRITE, SOURCE_TYPE_RADAR, GRANT),
    (NOT_ADMIN, WRITE, SOURCE_TYPE_UKRDC, DENY),
    (ADMIN, READ, SOURCE_TYPE_RADAR, GRANT),
    (ADMIN, READ, SOURCE_TYPE_UKRDC, GRANT),
    (ADMIN, WRITE, SOURCE_TYPE_RADAR, GRANT),
    (ADMIN, WRITE, SOURCE_TYPE_UKRDC, GRANT),
])
def test_has_object_permission(is_admin, action, source_type, expected):
    permission = RadarSourceObjectPermission()
    request = make_request(action)
    user = make_user([(Group(), ROLE.CLINICIAN)])
    user.is_admin = is_admin
    obj = make_obj(source_type)

    assert permission.has_object_permission(request, user, obj) == expected
