import json

import pytest

from radar_api.tests.fixtures import get_user, get_group
from radar.models.groups import GROUP_TYPE_OTHER, GROUP_CODE_NHS


@pytest.mark.parametrize(['username', 'expected'], [
    ('admin', True),
    ('hospital1_clinician', True),
    ('hospital1_admin', False),
    ('null', False),
])
def test_recruit_patient_search(app, username, expected):
    user = get_user(username)
    nhs_group = get_group(GROUP_TYPE_OTHER, GROUP_CODE_NHS)

    client = app.test_client()
    client.login(user)

    response = client.post('/recruit-patient-search', data={
        'first_name': 'John',
        'last_name': 'Smith',
        'date_of_birth': '1990-01-01',
        'number': '9434765919',
        'number_group': nhs_group.id
    })

    if expected:
        assert response.status_code == 200

        data = json.loads(response.data)

        assert len(data['patients']) == 0
    else:
        assert response.status_code == 403

    response = client.post('/recruit-patient-search', data={
        'first_name': 'John',
        'last_name': 'Smith',
        'date_of_birth': '1990-01-01',
        'number': '9434765870',
        'number_group': nhs_group.id
    })

    if expected:
        assert response.status_code == 200

        data = json.loads(response.data)

        assert len(data['patients']) == 1
    else:
        assert response.status_code == 403
