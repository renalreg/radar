import pytest

from radar_api.tests.fixtures import get_user, get_patient, get_group
from radar.models.groups import GROUP_TYPE_HOSPITAL


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'created_group_type', 'created_group_code', 'expected'], [
    ('admin', GROUP_TYPE_HOSPITAL, 'HOSPITAL2', GROUP_TYPE_HOSPITAL, 'HOSPITAL2', True),
])
def test_create_group_patient(app, username, group_type, group_code, created_group_type, created_group_code, expected):
    user = get_user(username)
    patient = get_patient(1)

    group = get_group(group_type, group_code)

    if created_group_type is not None:
        created_group = get_group(created_group_type, created_group_code)
        created_group_id = created_group.id
    else:
        created_group_id = None

    client = app.test_client()
    client.login(user)

    response = client.post('/group-patients', data={
        'patient': patient.id,
        'group': group.id,
        'created_group': created_group_id,
        'from_date': '2015-01-01'
    })

    print response.data
