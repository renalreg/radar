import json

import pytest
from sqlalchemy import func

from radar.models.groups import Group, GroupPatient, GROUP_TYPE_COHORT, GROUP_TYPE_HOSPITAL, GroupUser, GROUP_CODE_RADAR, GROUP_TYPE_OTHER
from radar.models.patients import Patient
from radar.models.users import User
from radar.models.source_types import SOURCE_TYPE_RADAR
from radar.models.patient_demographics import PatientDemographics
from radar.roles import ROLE


@pytest.fixture
def admin(session):
    u = User()
    u.username = 'admin'
    u.password = 'password'
    u.is_admin = True
    session.add(u)
    session.commit()
    return u


@pytest.fixture
def cohort_user(session, cohort_group, admin):
    u = User()
    u.username = 'cohort_user'
    u.password = 'password'
    session.add(u)

    gu = GroupUser()
    gu.group = cohort_group
    gu.user = u
    gu.role = ROLE.RESEARCHER
    gu.created_user = admin
    gu.modified_user = admin
    session.add(gu)

    session.commit()

    return u


@pytest.fixture
def hospital_user(session, hospital_group, admin):
    u = User()
    u.username = 'hospital_user'
    u.password = 'password'
    session.add(u)

    gu = GroupUser()
    gu.group = hospital_group
    gu.user = u
    gu.role = ROLE.CLINICIAN
    gu.created_user = admin
    gu.modified_user = admin
    session.add(gu)

    session.commit()

    return u


@pytest.fixture
def other_user(session, hospital_group, admin):
    u = User()
    u.username = 'other_user'
    u.password = 'password'
    session.add(u)
    session.commit()
    return u


@pytest.fixture
def patient(session, cohort_group, hospital_group, radar_group, admin):
    p = Patient()
    p.created_user = admin
    p.modified_user = admin
    session.add(p)

    d = PatientDemographics()
    d.patient = p
    d.source_group = hospital_group
    d.source_type = SOURCE_TYPE_RADAR
    d.first_name = 'John'
    d.last_name = 'Smith'
    d.created_user = admin
    d.modified_user = admin
    session.add(d)

    rp = GroupPatient()
    rp.group = radar_group
    rp.patient = p
    rp.from_date = func.now()
    rp.created_user = admin
    rp.modified_user = admin
    session.add(rp)

    cp = GroupPatient()
    cp.group = cohort_group
    cp.patient = p
    cp.from_date = func.now()
    cp.created_user = admin
    cp.modified_user = admin
    session.add(cp)

    hp = GroupPatient()
    hp.group = hospital_group
    hp.patient = p
    hp.from_date = func.now()
    hp.created_user = admin
    hp.modified_user = admin
    session.add(hp)

    session.commit()

    return p


@pytest.fixture
def radar_group(session):
    g = Group()
    g.type = GROUP_TYPE_OTHER
    g.code = GROUP_CODE_RADAR
    g.name = 'RaDaR'
    g.short_name = 'RaDaR'
    session.add(g)
    session.commit()
    return g


@pytest.fixture
def cohort_group(session):
    g = Group()
    g.type = GROUP_TYPE_COHORT
    g.code = 'COHORT1'
    g.name = 'Cohort 1'
    g.short_name = 'Cohort 1'
    session.add(g)
    session.commit()
    return g


@pytest.fixture
def hospital_group(session):
    g = Group()
    g.type = GROUP_TYPE_HOSPITAL
    g.code = 'HOSPITAL1'
    g.name = 'Hospital 1'
    g.short_name = 'Hospital 1'
    session.add(g)
    session.commit()
    return g


def test_as_admin_user(app, patient, admin):
    client = app.test_client()
    client.login(admin)

    response = client.get('/patients')

    data = json.loads(response.data)

    assert len(data['data']) == 1
    assert data['data'][0]['first_name'] == 'John'


def test_as_cohort_user(app, patient, cohort_user, session):
    client = app.test_client()
    client.login(cohort_user)

    response = client.get('/patients')

    data = json.loads(response.data)

    assert len(data['data']) == 1
    assert 'first_name' not in data['data'][0]


def test_as_hospital_user(app, patient, hospital_user):
    client = app.test_client()
    client.login(hospital_user)

    response = client.get('/patients')

    data = json.loads(response.data)

    assert len(data['data']) == 1
    assert data['data'][0]['first_name'] == 'John'


def test_as_other_user(app, patient, other_user):
    client = app.test_client()
    client.login(other_user)

    response = client.get('/patients')

    data = json.loads(response.data)

    assert len(data['data']) == 0
