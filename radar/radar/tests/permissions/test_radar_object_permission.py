import pytest
from radar.models import DataSource, Organisation, ORGANISATION_TYPE_OTHER, ORGANISATION_CODE_RADAR, \
    DATA_SOURCE_TYPE_RADAR, DATA_SOURCE_TYPE_PV, Medication, ORGANISATION_TYPE_UNIT
from radar.permissions import RadarObjectPermission
from radar.tests.permissions.helpers import MockRequest, make_user


READ = 0
WRITE = 1

EXTERNAL = 0
RADAR = 1

DENY = False
GRANT = True


def make_request(action):
    if action == READ:
        method = 'GET'
    else:
        method = 'POST'

    return MockRequest(method)


def make_obj(source):
    data_source = DataSource()
    organisation = Organisation()
    data_source.organisation = organisation

    if source == RADAR:
        data_source.type = DATA_SOURCE_TYPE_RADAR
        organisation.code = ORGANISATION_CODE_RADAR
        organisation.type = ORGANISATION_TYPE_OTHER
    else:
        data_source.type = DATA_SOURCE_TYPE_PV
        organisation.code = 'REE01'
        organisation.type = ORGANISATION_TYPE_UNIT

    obj = Medication()
    obj.data_source = data_source

    return obj


@pytest.mark.parametrize(['action', 'source', 'expected'], [
    (READ, RADAR, GRANT),
    (READ, EXTERNAL, GRANT),
    (WRITE, RADAR, GRANT),
    (WRITE, EXTERNAL, DENY),
])
def test_has_object_permission(action, source, expected):
    permission = RadarObjectPermission()
    request = make_request(action)
    user = make_user()
    obj = make_obj(source)

    assert permission.has_object_permission(request, user, obj) == expected
