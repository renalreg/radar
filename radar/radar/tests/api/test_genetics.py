import json
import itertools
from datetime import datetime

import pytest
import pytz

from radar.models.genetics import Genetics
from radar.database import db
from radar_api.tests.fixtures import get_user, get_patient, get_group, set_default_users
from radar.models.groups import GROUP_TYPE, GROUP_CODE_RADAR


def create_genetics(patient, group, **kwargs):
    kwargs.setdefault('date_sent', datetime(2016, 1, 1))
    set_default_users(kwargs)

    genetics = Genetics(
        patient=patient,
        group=group,
        **kwargs
    )
    db.session.add(genetics)

    return genetics


def get_read_list_args():
    usernames = [
        'admin', 'hospital1_clinician', 'hospital2_clinician',
        'cohort1_researcher', 'cohort2_researcher', 'null',
        'hospital1_it'
    ]
    cohort1_group = (GROUP_TYPE.COHORT, 'COHORT1')
    cohort2_group = (GROUP_TYPE.COHORT, 'COHORT2')
    groups = [cohort1_group, cohort2_group]

    for username, group in itertools.product(usernames, groups):
        if username == 'admin':
            expected = True
        elif username == 'hospital1_clinician':
            expected = True
        elif username == 'cohort1_researcher':
            expected = group == cohort1_group
        else:
            expected = False

        yield username, group[0], group[1], expected


def get_read_args():
    return get_read_list_args()


def get_create_args():
    radar_group = (GROUP_TYPE.OTHER, GROUP_CODE_RADAR)
    hospital1_group = (GROUP_TYPE.HOSPITAL, 'HOSPITAL1')
    cohort1_group = (GROUP_TYPE.COHORT, 'COHORT1')
    cohort2_group = (GROUP_TYPE.COHORT, 'COHORT2')

    usernames = [
        'admin', 'hospital1_clinician', 'hospital2_clinician',
        'cohort1_researcher', 'cohort2_researcher', 'null',
        'hospital1_it'
    ]
    groups = [radar_group, hospital1_group, cohort1_group, cohort2_group]

    for username, group in itertools.product(usernames, groups):
        if group != cohort1_group:
            expected = False
        elif username == 'admin':
            expected = True
        elif username == 'hospital1_clinician':
            expected = True
        else:
            expected = False

        yield username, group[0], group[1], expected


def get_delete_args():
    return get_update_args()


def get_update_args():
    group_type = GROUP_TYPE.COHORT
    group_code = 'COHORT1'

    usernames = [
        'admin', 'hospital1_clinician', 'hospital2_clinician',
        'cohort1_researcher', 'cohort2_researcher', 'null',
        'hospital1_it'
    ]

    for username in usernames:
        if username == 'admin':
            expected = 200
        elif username == 'hospital1_clinician':
            expected = 200
        elif username == 'cohort1_researcher':
            expected = 403
        else:
            expected = 404

        yield username, group_type, group_code, expected


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'expected'], get_read_list_args())
def test_read_genetics_list(app, username, group_type, group_code, expected):
    user = get_user(username)
    patient = get_patient(1)
    group = get_group(group_type, group_code)
    create_genetics(patient, group)
    db.session.commit()

    client = app.test_client()
    client.login(user)

    response = client.get('/genetics?patient=%s' % patient.id)

    data = json.loads(response.data)

    assert response.status_code == 200

    if expected:
        assert len(data['data']) == 1
    else:
        assert len(data['data']) == 0


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'expected'], get_read_args())
def test_read_genetics(app, username, group_type, group_code, expected):
    user = get_user(username)
    patient = get_patient(1)
    group = get_group(group_type, group_code)
    genetics = create_genetics(patient, group)
    db.session.commit()

    client = app.test_client()
    client.login(user)

    response = client.get('/genetics/%s' % genetics.id)

    if expected:
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['id'] == genetics.id
    else:
        assert response.status_code == 404


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'expected'], get_delete_args())
def test_delete_genetics(app, username, group_type, group_code, expected):
    user = get_user(username)
    patient = get_patient(1)
    group = get_group(group_type, group_code)
    genetics = create_genetics(patient, group)
    db.session.commit()

    client = app.test_client()
    client.login(user)

    response = client.delete('/genetics/%s' % genetics.id)

    genetics = Genetics.query.get(genetics.id)

    assert response.status_code == expected

    if expected == 200:
        # Check the genetics were deleted
        assert genetics is None
    else:
        # Check the genetics were't deleted
        assert genetics is not None


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'expected'], get_create_args())
def test_create_genetics(app, username, group_type, group_code, expected):
    user = get_user(username)
    patient = get_patient(1)
    group = get_group(group_type, group_code)
    db.session.commit()

    data = {
        'patient': patient.id,
        'group': group.id,
        'date_sent': '2016-01-01',
    }

    client = app.test_client()
    client.login(user)

    response = client.post('/genetics', data=data)

    if expected:
        assert response.status_code == 200

        data = json.loads(response.data)

        genetics = Genetics.query.get(data['id'])

        # Check the genetics were created
        assert genetics is not None
    else:
        assert response.status_code == 403

        # Check the genetics weren't created
        assert Genetics.query.filter(Genetics.patient_id == patient.id).count() == 0


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'expected'], get_update_args())
def test_update_genetics(app, username, group_type, group_code, expected):
    user = get_user(username)
    patient = get_patient(1)
    group = get_group(group_type, group_code)
    genetics = create_genetics(patient, group, date_sent=datetime(2016, 1, 1))
    db.session.commit()

    data = {
        'id': genetics.id,
        'date_sent': '2016-01-02'
    }

    client = app.test_client()
    client.login(user)

    response = client.put('/genetics/%s' % genetics.id, data=data)

    assert response.status_code == expected

    db.session.refresh(genetics)

    if expected == 200:
        # Check the genetics were updated
        assert genetics.date_sent == datetime(2016, 1, 2, tzinfo=pytz.UTC)
    else:
        # Check the genetics weren't updated
        assert genetics.date_sent == datetime(2016, 1, 1, tzinfo=pytz.UTC)
