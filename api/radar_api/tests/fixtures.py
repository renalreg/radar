from datetime import datetime

from sqlalchemy import func

from radar.database import db
from radar.models.users import User
from radar.models.groups import Group, GroupUser, GroupPatient, GROUP_TYPE_OTHER, GROUP_CODE_RADAR, GROUP_TYPE_HOSPITAL, GROUP_TYPE_COHORT
from radar.models.patient_demographics import PatientDemographics
from radar.models.patients import Patient
from radar.roles import ROLE
from radar.models.source_types import SOURCE_TYPE_RADAR


def create_user(username, **kwargs):
    kwargs.setdefault('password', 'password')

    u = User(
        username=username,
        **kwargs
    )
    db.session.add(u)

    return u


def get_user(username):
    return User.query.filter(User.username == username).one()


def get_cohort(code):
    return get_group(GROUP_TYPE_COHORT, code)


def get_hospital(code):
    return get_group(GROUP_TYPE_HOSPITAL, code)


def get_group(type, code):
    return Group.query.filter(Group.type == type, Group.code == code).one()


def get_admin():
    return get_user('admin')


def get_patient(patient_id):
    return Patient.query.get(patient_id)


def set_default_users(options):
    options['created_user'] = options.get('created_user') or get_admin()
    options['modified_user'] = options.get('modified_user') or get_admin()


def set_default_source(options):
    options['source_group'] = options.get('source_group') or get_group(GROUP_TYPE_OTHER, GROUP_CODE_RADAR)
    options.setdefault('source_type', SOURCE_TYPE_RADAR)


def add_user_to_group(user, group, role, **kwargs):
    set_default_users(kwargs)

    gu = GroupUser(
        user=user,
        group=group,
        role=role,
        **kwargs
    )
    db.session.add(gu)

    return gu


def add_patient_to_group(patient, group, **kwargs):
    kwargs.setdefault('from_date', func.now())
    set_default_users(kwargs)

    gp = GroupPatient(
        patient=patient,
        group=group,
        **kwargs
    )
    db.session.add(gp)

    return gp


def create_patient(**kwargs):
    set_default_users(kwargs)

    p = Patient(**kwargs)
    db.session.add(p)

    return p


def create_demographics(patient, **kwargs):
    kwargs.setdefault('first_name', 'JOHN')
    kwargs.setdefault('last_name', 'SMITH')
    kwargs.setdefault('gender', 1)
    kwargs.setdefault('date_of_birth', datetime(1990, 1, 1))
    set_default_users(kwargs)
    set_default_source(kwargs)

    d = PatientDemographics(
        patient=patient,
        **kwargs
    )
    db.session.add(d)

    return d


def create_group(type, code, **kwargs):
    kwargs.setdefault('name', 'Test')
    kwargs.setdefault('short_name', 'Test')

    g = Group(
        type=type,
        code=code,
        **kwargs
    )
    db.session.add(g)

    return g


def create_cohort(code, **kwargs):
    return create_group(GROUP_TYPE_COHORT, code, **kwargs)


def create_hospital(code, **kwargs):
    return create_group(GROUP_TYPE_HOSPITAL, code, **kwargs)


def create_fixtures():
    create_user('admin', is_admin=True)
    create_user('null')

    radar_group = create_group(GROUP_TYPE_OTHER, GROUP_CODE_RADAR)
    cohort1_group = create_cohort('COHORT1')
    cohort2_group = create_cohort('COHORT2')
    hospital1_group = create_hospital('HOSPITAL1')
    hospital2_group = create_hospital('HOSPITAL2')

    cohort1_user = create_user('cohort1')
    add_user_to_group(cohort1_user, cohort1_group, ROLE.RESEARCHER)

    cohort2_user = create_user('cohort2')
    add_user_to_group(cohort2_user, cohort2_group, ROLE.RESEARCHER)

    hospital1_user = create_user('hospital1')
    add_user_to_group(hospital1_user, hospital1_group, ROLE.CLINICIAN)

    hospital2_user = create_user('hospital2')
    add_user_to_group(hospital2_user, hospital2_group, ROLE.CLINICIAN)

    patient1 = create_patient(id=1)
    add_patient_to_group(patient1, radar_group)
    add_patient_to_group(patient1, cohort1_group)
    add_patient_to_group(patient1, hospital1_group)
    create_demographics(patient1)

    patient2 = create_patient(id=2)
    add_patient_to_group(patient2, radar_group)
    add_patient_to_group(patient2, cohort1_group)
    add_patient_to_group(patient2, hospital1_group)
