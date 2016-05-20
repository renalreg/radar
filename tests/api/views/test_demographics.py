import json
import itertools

import pytest

from radar.database import db
from radar.models.groups import GROUP_TYPE, GROUP_CODE_RADAR
from radar.models.patient_demographics import PatientDemographics
from radar.models.source_types import SOURCE_TYPE_RADAR, SOURCE_TYPE_UKRDC
from tests.api.views.fixtures import get_user, get_patient, get_group, create_demographics


def get_read_list_args():
    usernames = [
        'admin', 'hospital1_clinician', 'hospital2_clinician',
        'cohort1_researcher', 'cohort2_researcher', 'null',
        'hospital1_it', 'cohort1_senior_researcher'
    ]
    groups = [
        (GROUP_TYPE.OTHER, GROUP_CODE_RADAR),
        (GROUP_TYPE.HOSPITAL, 'HOSPITAL1'),
        (GROUP_TYPE.HOSPITAL, 'HOSPITAL2'),
    ]
    source_types = [SOURCE_TYPE_RADAR, SOURCE_TYPE_UKRDC]

    for username, group, source_type in itertools.product(usernames, groups, source_types):
        if username == 'admin':
            expected = True
            expected_demographics = True
        elif username == 'hospital1_clinician':
            expected = True
            expected_demographics = True
        elif username == 'cohort1_researcher':
            expected = True
            expected_demographics = False
        elif username == 'cohort1_senior_researcher':
            expected = True
            expected_demographics = True
        else:
            expected = False
            expected_demographics = False

        yield username, group[0], group[1], source_type, expected, expected_demographics


def get_read_args():
    return get_read_list_args()


def get_create_args():
    radar_group = (GROUP_TYPE.OTHER, GROUP_CODE_RADAR)
    hospital1_group = (GROUP_TYPE.HOSPITAL, 'HOSPITAL1')
    cohort1_group = (GROUP_TYPE.COHORT, 'COHORT1')

    usernames = [
        'admin', 'hospital1_clinician', 'hospital2_clinician',
        'cohort1_researcher', 'cohort2_researcher', 'null',
        'hospital1_it', 'cohort1_senior_researcher'
    ]
    groups = [radar_group, hospital1_group, cohort1_group]
    source_types = [SOURCE_TYPE_RADAR, SOURCE_TYPE_UKRDC]

    for username, group, source_type in itertools.product(usernames, groups, source_types):
        if username == 'admin':
            expected = True
        elif username == 'hospital1_clinician':
            expected = source_type == SOURCE_TYPE_RADAR and group == radar_group
        else:
            expected = False

        yield username, group[0], group[1], source_type, expected


def get_delete_args():
    return get_update_args()


def get_update_args():
    radar_group = (GROUP_TYPE.OTHER, GROUP_CODE_RADAR)
    hospital1_group = (GROUP_TYPE.HOSPITAL, 'HOSPITAL1')

    usernames = [
        'admin', 'hospital1_clinician', 'hospital1_clinician',
        'cohort1_researcher', 'cohort2_researcher', 'null',
        'hospital1_it', 'cohort1_senior_researcher'
    ]
    groups = [radar_group, hospital1_group]
    source_types = [SOURCE_TYPE_RADAR, SOURCE_TYPE_UKRDC]

    for username, group, source_type in itertools.product(usernames, groups, source_types):
        if username == 'admin':
            expected = 200
        elif username == 'hospital1_clinician':
            if source_type == SOURCE_TYPE_RADAR and group == radar_group:
                expected = 200
            else:
                expected = 403
        elif username in ['cohort1_researcher', 'cohort1_senior_researcher']:
            expected = 403
        else:
            expected = 404

        yield username, group[0], group[1], source_type, expected


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'source_type', 'expected', 'expected_demographics'], get_read_list_args())
def test_read_demographics_list(api, username, group_type, group_code, source_type, expected, expected_demographics):
    user = get_user(username)
    patient = get_patient(2)
    group = get_group(group_type, group_code)
    create_demographics(patient, source_group=group, source_type=source_type)
    db.session.commit()

    client = api.test_client()
    client.login(user)

    response = client.get('/patient-demographics?patient=%s' % patient.id)

    data = json.loads(response.data)

    assert response.status_code == 200

    if expected:
        assert len(data['data']) == 1

        if expected_demographics:
            assert data['data'][0]['first_name'] == 'JOHN'
        else:
            assert 'first_name' not in data['data'][0]
    else:
        assert len(data['data']) == 0


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'source_type', 'expected', 'expected_demographics'], get_read_args())
def test_read_demographics(api, username, group_type, group_code, source_type, expected, expected_demographics):
    user = get_user(username)
    patient = get_patient(2)
    group = get_group(group_type, group_code)
    demographics = create_demographics(patient, source_group=group, source_type=source_type, first_name='JOHN', last_name='SMITH')
    db.session.commit()

    client = api.test_client()
    client.login(user)

    response = client.get('/patient-demographics/%s' % demographics.id)

    if expected:
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['id'] == demographics.id

        if expected_demographics:
            assert data['first_name'] == 'JOHN'
        else:
            assert 'first_name' not in data
    else:
        assert response.status_code == 404


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'source_type', 'expected'], get_delete_args())
def test_delete_demographics(api, username, group_type, group_code, source_type, expected):
    user = get_user(username)
    patient = get_patient(2)
    group = get_group(group_type, group_code)
    demographics = create_demographics(patient, source_group=group, source_type=source_type)
    db.session.commit()

    client = api.test_client()
    client.login(user)

    response = client.delete('/patient-demographics/%s' % demographics.id)

    demographics = PatientDemographics.query.get(demographics.id)

    assert response.status_code == expected

    if expected == 200:
        # Check the demographics were deleted
        assert demographics is None
    else:
        # Check the demographics were't deleted
        assert demographics is not None


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'source_type', 'expected'], get_create_args())
def test_create_demographics(api, username, group_type, group_code, source_type, expected):
    user = get_user(username)
    patient = get_patient(2)
    group = get_group(group_type, group_code)
    db.session.commit()

    data = {
        'patient': patient.id,
        'source_group': group.id,
        'source_type': source_type,
        'first_name': 'BRUCE',
        'last_name': 'WAYNE',
        'gender': 1,
        'date_of_birth': '2016-01-01',
    }

    client = api.test_client()
    client.login(user)

    response = client.post('/patient-demographics', data=data)

    if expected:
        assert response.status_code == 200

        data = json.loads(response.data)

        demographics = PatientDemographics.query.get(data['id'])

        # Check the demographics were created
        assert demographics is not None
    else:
        assert response.status_code == 403

        # Check the demographics weren't created
        assert PatientDemographics.query.filter(PatientDemographics.patient_id == patient.id).count() == 0


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'source_type', 'expected'], get_update_args())
def test_update_demographics(api, username, group_type, group_code, source_type, expected):
    user = get_user(username)
    patient = get_patient(2)
    group = get_group(group_type, group_code)
    demographics = create_demographics(patient, source_group=group, source_type=source_type, first_name='JOHN', last_name='SMITH')
    db.session.commit()

    data = {
        'id': demographics.id,
        'first_name': 'BRUCE',
        'last_name': 'WAYNE',
    }

    client = api.test_client()
    client.login(user)

    response = client.patch('/patient-demographics/%s' % demographics.id, data=data)

    assert response.status_code == expected

    db.session.refresh(demographics)

    if expected == 200:
        # Check the demographics were updated
        assert demographics.first_name == 'BRUCE'
        assert demographics.last_name == 'WAYNE'
    else:
        # Check the demographics weren't updated
        assert demographics.first_name == 'JOHN'
        assert demographics.last_name == 'SMITH'
