import pytest

from radar_api.tests.fixtures import get_user, get_patient, get_group
from radar.models.groups import GROUP_TYPE_HOSPITAL, GROUP_TYPE_COHORT


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'created_group_type', 'created_group_code', 'expected'], [
    ('admin', GROUP_TYPE_HOSPITAL, 'HOSPITAL2', GROUP_TYPE_HOSPITAL, 'HOSPITAL2', 200),

    ('hospital_clinician', GROUP_TYPE_HOSPITAL, 'HOSPITAL2', GROUP_TYPE_HOSPITAL, 'HOSPITAL2', 200),
    ('hospital_clinician', GROUP_TYPE_HOSPITAL, 'HOSPITAL2', GROUP_TYPE_HOSPITAL, 'HOSPITAL1', 200),
    ('hospital_clinician', GROUP_TYPE_HOSPITAL, 'HOSPITAL2', GROUP_TYPE_COHORT, 'COHORT2', 403),
    ('hospital_clinician', GROUP_TYPE_HOSPITAL, 'HOSPITAL1', GROUP_TYPE_HOSPITAL, 'HOSPITAL2', 422),
    ('hospital_clinician', GROUP_TYPE_COHORT, 'COHORT2', GROUP_TYPE_HOSPITAL, 'HOSPITAL2', 200),
    ('hospital_clinician', GROUP_TYPE_COHORT, 'COHORT2', GROUP_TYPE_HOSPITAL, 'HOSPITAL1', 200),
    ('hospital_clinician', GROUP_TYPE_COHORT, 'COHORT2', GROUP_TYPE_COHORT, 'COHORT2', 403),
    ('hospital_clinician', GROUP_TYPE_COHORT, 'COHORT1', GROUP_TYPE_HOSPITAL, 'HOSPITAL2', 422),

    ('hospital1_clinician', GROUP_TYPE_HOSPITAL, 'HOSPITAL2', GROUP_TYPE_HOSPITAL, 'HOSPITAL1', 403),
    ('hospital1_clinician', GROUP_TYPE_HOSPITAL, 'HOSPITAL1', GROUP_TYPE_HOSPITAL, 'HOSPITAL1', 422),
    ('hospital1_clinician', GROUP_TYPE_COHORT, 'COHORT2', GROUP_TYPE_HOSPITAL, 'HOSPITAL1', 200),
    ('hospital1_clinician', GROUP_TYPE_COHORT, 'COHORT2', GROUP_TYPE_HOSPITAL, 'HOSPITAL2', 403),
    ('hospital1_clinician', GROUP_TYPE_COHORT, 'COHORT1', GROUP_TYPE_HOSPITAL, 'HOSPITAL1', 422),

    ('hospital2_clinician', GROUP_TYPE_COHORT, 'COHORT2', GROUP_TYPE_HOSPITAL, 'HOSPITAL2', 403),
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

    assert response.status_code == expected
