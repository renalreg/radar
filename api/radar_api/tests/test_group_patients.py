import json

import pytest

from radar_api.tests.fixtures import get_user, get_patient, get_group, create_patient, add_patient_to_group
from radar.models.groups import GROUP_TYPE, GROUP_CODE_RADAR


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'created_group_type', 'created_group_code', 'expected'], [
    ('admin', GROUP_TYPE.HOSPITAL, 'HOSPITAL2', GROUP_TYPE.HOSPITAL, 'HOSPITAL2', 200),

    ('hospital_clinician', GROUP_TYPE.HOSPITAL, 'HOSPITAL2', GROUP_TYPE.HOSPITAL, 'HOSPITAL2', 200),
    ('hospital_clinician', GROUP_TYPE.HOSPITAL, 'HOSPITAL2', GROUP_TYPE.HOSPITAL, 'HOSPITAL1', 200),
    ('hospital_clinician', GROUP_TYPE.HOSPITAL, 'HOSPITAL2', GROUP_TYPE.COHORT, 'COHORT2', 403),
    ('hospital_clinician', GROUP_TYPE.HOSPITAL, 'HOSPITAL1', GROUP_TYPE.HOSPITAL, 'HOSPITAL2', 422),
    ('hospital_clinician', GROUP_TYPE.COHORT, 'COHORT2', GROUP_TYPE.HOSPITAL, 'HOSPITAL2', 200),
    ('hospital_clinician', GROUP_TYPE.COHORT, 'COHORT2', GROUP_TYPE.HOSPITAL, 'HOSPITAL1', 200),
    ('hospital_clinician', GROUP_TYPE.COHORT, 'COHORT2', GROUP_TYPE.COHORT, 'COHORT2', 403),
    ('hospital_clinician', GROUP_TYPE.COHORT, 'COHORT1', GROUP_TYPE.HOSPITAL, 'HOSPITAL2', 422),

    ('hospital1_clinician', GROUP_TYPE.HOSPITAL, 'HOSPITAL2', GROUP_TYPE.HOSPITAL, 'HOSPITAL1', 403),
    ('hospital1_clinician', GROUP_TYPE.HOSPITAL, 'HOSPITAL1', GROUP_TYPE.HOSPITAL, 'HOSPITAL1', 422),
    ('hospital1_clinician', GROUP_TYPE.COHORT, 'COHORT2', GROUP_TYPE.HOSPITAL, 'HOSPITAL1', 200),
    ('hospital1_clinician', GROUP_TYPE.COHORT, 'COHORT2', GROUP_TYPE.HOSPITAL, 'HOSPITAL2', 403),
    ('hospital1_clinician', GROUP_TYPE.COHORT, 'COHORT1', GROUP_TYPE.HOSPITAL, 'HOSPITAL1', 422),

    ('hospital2_clinician', GROUP_TYPE.COHORT, 'COHORT2', GROUP_TYPE.HOSPITAL, 'HOSPITAL2', 403),

    ('null', GROUP_TYPE.HOSPITAL, 'HOSPITAL2', GROUP_TYPE.HOSPITAL, 'HOSPITAL1', 403),
    ('null', GROUP_TYPE.COHORT, 'COHORT2', GROUP_TYPE.HOSPITAL, 'HOSPITAL1', 403),
])
def test_create_group_patient(app, username, group_type, group_code, created_group_type, created_group_code, expected):
    user = get_user(username)
    patient = get_patient(1)

    group = get_group(group_type, group_code)
    created_group = get_group(created_group_type, created_group_code)

    client = app.test_client()
    client.login(user)

    response = client.post('/group-patients', data={
        'patient': patient.id,
        'group': group.id,
        'created_group': created_group.id,
        'from_date': '2015-01-01'
    })

    assert response.status_code == expected


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'created_group_type', 'created_group_code', 'expected'], [
    ('admin', GROUP_TYPE.OTHER, GROUP_CODE_RADAR, GROUP_TYPE.HOSPITAL, 'HOSPITAL1', True),

    ('hospital1_clinician', GROUP_TYPE.COHORT, 'COHORT1', GROUP_TYPE.HOSPITAL, 'HOSPITAL1', True),
    ('hospital1_clinician', GROUP_TYPE.HOSPITAL, 'HOSPITAL1', GROUP_TYPE.HOSPITAL, 'HOSPITAL1', True),
    ('hospital1_clinician', GROUP_TYPE.HOSPITAL, 'HOSPITAL1', GROUP_TYPE.HOSPITAL, 'HOSPITAL2', True),
    ('hospital1_clinician', GROUP_TYPE.HOSPITAL, 'HOSPITAL2', GROUP_TYPE.HOSPITAL, 'HOSPITAL1', False),
    ('hospital1_clinician', GROUP_TYPE.OTHER, GROUP_CODE_RADAR, GROUP_TYPE.HOSPITAL, 'HOSPITAL1', False),

    ('null', GROUP_TYPE.HOSPITAL, 'HOSPITAL1', GROUP_TYPE.HOSPITAL, 'HOSPITAL1', False),
    ('null', GROUP_TYPE.COHORT, 'COHORT1', GROUP_TYPE.HOSPITAL, 'HOSPITAL1', False),
])
def test_delete_group_patient(app, username, group_type, group_code, created_group_type, created_group_code, expected):
    user = get_user(username)

    radar_group = get_group(GROUP_TYPE.OTHER, GROUP_CODE_RADAR)
    group = get_group(group_type, group_code)
    created_group = get_group(created_group_type, created_group_code)

    patient = create_patient()

    if group != radar_group:
        add_patient_to_group(patient, radar_group)

    group_patient = add_patient_to_group(patient, group, created_group=created_group)

    client = app.test_client()
    client.login(user)

    response = client.delete('/group-patients/%s' % group_patient.id)

    if expected:
        assert response.status_code == 200
    else:
        assert response.status_code == 403


@pytest.mark.parametrize(['username', 'expected'], [
    ('admin', 3),
    ('hospital1_clinician', 3),
    ('hospital2_clinician', 0),
    ('cohort1_researcher', 3),
    ('null', 0),
])
def test_read_group_patient_list(app, username, expected):
    user = get_user(username)
    patient = get_patient(1)

    client = app.test_client()
    client.login(user)

    response = client.get('/group-patients?patient=%s' % patient.id)

    assert response.status_code == 200

    data = json.loads(response.data)

    assert len(data['data']) == expected
