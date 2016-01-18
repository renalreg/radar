import json

import pytest

from radar_api.tests.fixtures import get_user

matrix = [
    ('admin', True, True),
    ('hospital1', True, True),
    ('cohort1', True, False),
    ('hospital2', False, False),
    ('cohort2', False, False),
    ('null', False, False),
]


@pytest.mark.parametrize(['username', 'expected', 'expected_demographics'], matrix)
def test_patient_read_list(app, username, expected, expected_demographics):
    user = get_user(username)

    client = app.test_client()
    client.login(user)

    response = client.get('/patients')

    data = json.loads(response.data)

    if expected:
        assert len(data['data']) == 2

        if expected_demographics:
            assert data['data'][0]['first_name'] == 'JOHN'
        else:
            assert 'first_name' not in data['data'][0]
    else:
        assert len(data['data']) == 0


@pytest.mark.parametrize(['username', 'expected', 'expected_demographics'], matrix)
def test_patient_read(app, username, expected, expected_demographics):
    user = get_user(username)

    client = app.test_client()
    client.login(user)

    response = client.get('/patients/1')

    if expected:
        assert response.status_code == 200

        data = json.loads(response.data)

        if expected_demographics:
            assert data['first_name'] == 'JOHN'
        else:
            assert 'first_name' not in data
    else:
        assert response.status_code == 404
