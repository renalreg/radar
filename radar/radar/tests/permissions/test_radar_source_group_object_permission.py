import pytest

from radar.models.medications import Medication
from radar.models.groups import Group, GROUP_TYPE_OTHER, GROUP_TYPE_HOSPITAL, GROUP_CODE_RADAR
from radar.models.source_types import SourceType, SOURCE_TYPE_RADAR, SOURCE_TYPE_UKRDC
from radar.permissions import RadarSourceObjectPermission
from radar.tests.permissions.helpers import MockRequest, make_user


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


def make_obj(source_type_id):
    source_type = SourceType(id=source_type_id)

    if source_type_id == SOURCE_TYPE_RADAR:
        source_group = Group(code=GROUP_CODE_RADAR, type=GROUP_TYPE_OTHER)
    else:
        source_group = Group(code='REE01', type=GROUP_TYPE_HOSPITAL)

    obj = Medication()
    obj.source_group = source_group
    obj.source_type = source_type

    return obj


@pytest.mark.parametrize(['is_admin', 'action', 'source_type_id', 'expected'], [
    (NOT_ADMIN, READ, SOURCE_TYPE_RADAR, GRANT),
    (NOT_ADMIN, READ, SOURCE_TYPE_UKRDC, GRANT),
    (NOT_ADMIN, WRITE, SOURCE_TYPE_RADAR, GRANT),
    (NOT_ADMIN, WRITE, SOURCE_TYPE_UKRDC, DENY),
    (ADMIN, READ, SOURCE_TYPE_RADAR, GRANT),
    (ADMIN, READ, SOURCE_TYPE_UKRDC, GRANT),
    (ADMIN, WRITE, SOURCE_TYPE_RADAR, GRANT),
    (ADMIN, WRITE, SOURCE_TYPE_UKRDC, GRANT),
])
def test_has_object_permission(is_admin, action, source_type_id, expected):
    permission = RadarSourceObjectPermission()
    request = make_request(action)
    user = make_user()
    user.is_admin = is_admin
    obj = make_obj(source_type_id)

    assert permission.has_object_permission(request, user, obj) == expected
