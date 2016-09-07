import json

import pytest

from tests.api.views.fixtures import get_user

matrix = [
    ('admin', True, True),
    ('hospital1_clinician', True, True),
    ('hospital1_it', False, False),
    ('hospital2_clinician', False, False),
    ('cohort1_researcher', True, False),
    ('cohort1_senior_researcher', True, True),
    ('cohort2_researcher', False, False),
    ('null', False, False),
]


@pytest.mark.parametrize(['username', 'expected', 'expected_demographics'], matrix)
def test_patient_read_list(api, username, expected, expected_demographics):
    user = get_user(username)

    client = api.test_client()
    client.login(user)

    response = client.get('/patients?id=1')

    data = json.loads(response.data)

    if expected:
        assert len(data['data']) == 1

        if expected_demographics:
            assert data['data'][0]['firstName'] == 'JOHN'
        else:
            assert 'firstName' not in data['data'][0]
    else:
        assert len(data['data']) == 0


@pytest.mark.parametrize(['username', 'expected', 'expected_demographics'], matrix)
def test_patient_read(api, username, expected, expected_demographics):
    user = get_user(username)

    client = api.test_client()
    client.login(user)

    response = client.get('/patients/1')

    if expected:
        assert response.status_code == 200

        data = json.loads(response.data)

        if expected_demographics:
            assert data['firstName'] == 'JOHN'
        else:
            assert 'firstName' not in data
    else:
        assert response.status_code == 404
