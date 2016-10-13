import json
import itertools

import pytest
from sqlalchemy import func

from radar.database import db
from radar.models.dialysis import Dialysis
from radar.models.groups import GROUP_TYPE, GROUP_CODE_RADAR
from radar.models.source_types import SOURCE_TYPE_MANUAL, SOURCE_TYPE_UKRDC
from tests.api.fixtures import (
    get_user,
    set_default_source,
    set_default_users,
    get_patient,
    get_group
)


def create_dialysis(patient, **kwargs):
    kwargs.setdefault('from_date', func.now())
    kwargs.setdefault('modality', 1)
    set_default_source(kwargs)
    set_default_users(kwargs)

    d = Dialysis(
        patient=patient,
        **kwargs
    )
    db.session.add(d)

    return d


def get_read_list_args():
    usernames = [
        'admin', 'hospital1_clinician', 'hospital2_clinician',
        'cohort1_researcher', 'cohort2_researcher', 'null',
        'hospital1_it'
    ]
    groups = [
        (GROUP_TYPE.SYSTEM, GROUP_CODE_RADAR),
        (GROUP_TYPE.HOSPITAL, 'HOSPITAL1'),
        (GROUP_TYPE.HOSPITAL, 'HOSPITAL2'),
    ]
    source_types = [SOURCE_TYPE_MANUAL, SOURCE_TYPE_UKRDC]

    for username, group, source_type in itertools.product(usernames, groups, source_types):
        if username == 'admin':
            expected = True
        elif username == 'hospital1_clinician':
            expected = True
        elif username == 'cohort1_researcher':
            expected = True
        else:
            expected = False

        yield username, group[0], group[1], source_type, expected


def get_read_args():
    return get_read_list_args()


def get_create_args():
    radar_group = (GROUP_TYPE.SYSTEM, GROUP_CODE_RADAR)
    hospital1_group = (GROUP_TYPE.HOSPITAL, 'HOSPITAL1')
    hospital2_group = (GROUP_TYPE.HOSPITAL, 'HOSPITAL2')
    cohort1_group = (GROUP_TYPE.COHORT, 'COHORT1')

    usernames = [
        'admin', 'hospital1_clinician', 'hospital2_clinician',
        'cohort1_researcher', 'cohort2_researcher', 'null',
        'hospital1_it'
    ]
    groups = [radar_group, hospital1_group, hospital2_group, cohort1_group]
    source_types = [SOURCE_TYPE_MANUAL, SOURCE_TYPE_UKRDC]

    for username, group, source_type in itertools.product(usernames, groups, source_types):
        if username == 'admin':
            expected = True
        elif username == 'hospital1_clinician':
            expected = source_type == SOURCE_TYPE_MANUAL and group in (radar_group, hospital1_group)
        else:
            expected = False

        yield username, group[0], group[1], source_type, expected


def get_delete_args():
    return get_update_args()


def get_update_args():
    radar_group = (GROUP_TYPE.SYSTEM, GROUP_CODE_RADAR)
    hospital1_group = (GROUP_TYPE.HOSPITAL, 'HOSPITAL1')
    hospital2_group = (GROUP_TYPE.HOSPITAL, 'HOSPITAL2')

    usernames = [
        'admin', 'hospital1_clinician', 'hospital2_clinician',
        'cohort1_researcher', 'cohort2_researcher', 'null',
        'hospital1_it'
    ]
    groups = [radar_group, hospital1_group, hospital2_group]
    source_types = [SOURCE_TYPE_MANUAL, SOURCE_TYPE_UKRDC]

    for username, group, source_type in itertools.product(usernames, groups, source_types):
        if username == 'admin':
            expected = 200
        elif username == 'hospital1_clinician':
            if source_type == SOURCE_TYPE_MANUAL and group in (radar_group, hospital1_group):
                expected = 200
            else:
                expected = 403
        elif username == 'cohort1_researcher':
            expected = 403
        else:
            expected = 404

        yield username, group[0], group[1], source_type, expected


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'source_type', 'expected'], get_read_list_args())
def test_read_dialysis_list(api, username, group_type, group_code, source_type, expected):
    user = get_user(username)
    patient = get_patient(1)
    group = get_group(group_type, group_code)
    create_dialysis(patient, source_group=group, source_type=source_type)
    db.session.commit()

    client = api.test_client()
    client.login(user)

    response = client.get('/dialysis')

    data = json.loads(response.data)

    assert response.status_code == 200

    if expected:
        assert len(data['data']) == 1
    else:
        assert len(data['data']) == 0


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'source_type', 'expected'], get_read_args())
def test_read_dialysis(api, username, group_type, group_code, source_type, expected):
    user = get_user(username)
    patient = get_patient(1)
    group = get_group(group_type, group_code)
    dialysis = create_dialysis(patient, source_group=group, source_type=source_type)
    db.session.commit()

    client = api.test_client()
    client.login(user)

    response = client.get('/dialysis/%s' % dialysis.id)

    if expected:
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['id'] == dialysis.id
    else:
        assert response.status_code == 404


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'source_type', 'expected'], get_delete_args())
def test_delete_dialysis(api, username, group_type, group_code, source_type, expected):
    user = get_user(username)
    patient = get_patient(1)
    group = get_group(group_type, group_code)
    dialysis = create_dialysis(patient, source_group=group, source_type=source_type)
    db.session.commit()

    client = api.test_client()
    client.login(user)

    response = client.delete('/dialysis/%s' % dialysis.id)

    dialysis = Dialysis.query.get(dialysis.id)

    assert response.status_code == expected

    if expected == 200:
        # Check the dialysis was deleted
        assert dialysis is None
    else:
        # Check the dialysis wasn't deleted
        assert dialysis is not None


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'source_type', 'expected'], get_create_args())
def test_create_dialysis(api, username, group_type, group_code, source_type, expected):
    user = get_user(username)
    patient = get_patient(1)
    group = get_group(group_type, group_code)
    db.session.commit()

    data = {
        'patient': patient.id,
        'source_group': group.id,
        'source_type': source_type,
        'from_date': '2016-01-01',
        'modality': 1
    }

    client = api.test_client()
    client.login(user)

    response = client.post('/dialysis', data=data)

    if expected:
        assert response.status_code == 200

        data = json.loads(response.data)

        dialysis = Dialysis.query.get(data['id'])

        # Check the dialysis was created
        assert dialysis is not None
    else:
        assert response.status_code == 403

        # Check the dialysis wasn't created
        assert Dialysis.query.count() == 0


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'source_type', 'expected'], get_update_args())
def test_update_dialysis(api, username, group_type, group_code, source_type, expected):
    user = get_user(username)
    patient = get_patient(1)
    group = get_group(group_type, group_code)
    dialysis = create_dialysis(patient, source_group=group, source_type=source_type, modality=1)
    db.session.commit()

    data = {
        'id': dialysis.id,
        'modality': 2,
    }

    client = api.test_client()
    client.login(user)

    response = client.patch('/dialysis/%s' % dialysis.id, data=data)

    assert response.status_code == expected

    db.session.refresh(dialysis)

    if expected == 200:
        # Check the dialysis was updated
        assert dialysis.modality == 2
    else:
        # Check the dialysis wasn't updated
        assert dialysis.modality == 1
