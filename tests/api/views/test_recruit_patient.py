import itertools
import json

import pytest

from radar.models.groups import GROUP_CODE_NHS, GROUP_TYPE
from tests.api.fixtures import get_cohort, get_group, get_hospital, get_user


@pytest.mark.parametrize(['username', 'expected'], [
    ('admin', True),
    ('hospital1_clinician', True),
    ('hospital1_admin', False),
    ('null', False),
])
def test_recruit_patient_search(api, username, expected):
    user = get_user(username)
    nhs_group = get_group(GROUP_TYPE.OTHER, GROUP_CODE_NHS)

    client = api.test_client()
    client.login(user)

    response = client.post('/recruit-patient-search', data={
        'first_name': 'John',
        'last_name': 'Smith',
        'gender': 1,
        'date_of_birth': '1990-01-01',
        'number': '9434765919',
        'number_group': nhs_group.id
    })

    if expected:
        assert response.status_code == 200

        data = json.loads(response.data)

        assert not data['patient']
    else:
        assert response.status_code == 403

    response = client.post('/recruit-patient-search', data={
        'first_name': 'John',
        'last_name': 'Smith',
        'gender': 1,
        'date_of_birth': '1990-01-01',
        'number': '9434765870',
        'number_group': nhs_group.id
    })

    if expected:
        assert response.status_code == 200

        data = json.loads(response.data)

        assert data['patient']
    else:
        assert response.status_code == 403


def get_recruit_patient_args():
    usernames = ['admin', 'hospital1_clinician', 'cohort1_researcher', 'null']
    cohorts = ['COHORT1', 'COHORT2']
    hospitals = ['HOSPITAL1', 'HOSPITAL2']

    for username, cohort_code, hospital_code in itertools.product(usernames, cohorts, hospitals):
        if username == 'admin':
            expected = True
        elif username == 'hospital1_clinician':
            expected = hospital_code == 'HOSPITAL1'
        else:
            expected = False

        yield username, cohort_code, hospital_code, expected


@pytest.mark.parametrize(['username', 'cohort_code', 'hospital_code', 'expected'], get_recruit_patient_args())
def test_recruit_patient(api, username, cohort_code, hospital_code, expected):
    user = get_user(username)
    cohort_group = get_cohort(cohort_code)
    hospital_group = get_hospital(hospital_code)
    nhs_group = get_group(GROUP_TYPE.OTHER, GROUP_CODE_NHS)

    client = api.test_client()
    client.login(user)

    response = client.post('/recruit-patient', data={
        'first_name': 'Bruce',
        'last_name': 'Wayne',
        'date_of_birth': '1990-01-01',
        'gender': 1,
        'cohort_group': cohort_group.id,
        'hospital_group': hospital_group.id,
        'number': '9434765919',
        'number_group': nhs_group.id
    })

    if expected:
        assert response.status_code == 200
    else:
        assert response.status_code == 403
