from datetime import datetime

from radar.database import db
from radar.models.demographics import Ethnicity, Nationality
from radar.models.groups import (
    Group,
    GROUP_CODE_NHS,
    GROUP_CODE_RADAR,
    GROUP_TYPE,
    GroupPatient,
    GroupUser,
)
from radar.models.patient_demographics import PatientDemographics
from radar.models.patient_numbers import PatientNumber
from radar.models.patients import Patient
from radar.models.source_types import SOURCE_TYPE_MANUAL
from radar.models.users import User
from radar.roles import ROLE


def create_user(username, **kwargs):
    kwargs.setdefault('first_name', 'Foo')
    kwargs.setdefault('last_name', 'Bar')
    kwargs.setdefault('email', 'foo@example.org')
    kwargs.setdefault('password', 'password')

    u = User(
        username=username,
        **kwargs
    )
    db.session.add(u)
    db.session.flush()

    u.created_user = u
    u.modified_user = u

    return u


def get_user(username):
    return User.query.filter(User.username == username).one()


def get_cohort(code):
    return get_group(GROUP_TYPE.COHORT, code)


def get_hospital(code):
    return get_group(GROUP_TYPE.HOSPITAL, code)


def get_group(type, code):
    return Group.query.filter(Group.type == type, Group.code == code).one()


def get_admin():
    return get_user('admin')


def get_patient(patient_id):
    return Patient.query.get(patient_id)


def get_nationality(nationality_id):
    return Nationality.query.get(nationality_id)


def get_ethnicity(ethnicity_id):
    return Ethnicity.query.get(ethnicity_id)


def set_default_users(options):
    options['created_user'] = options.get('created_user') or get_admin()
    options['modified_user'] = options.get('modified_user') or get_admin()


def set_default_source(options):
    options['source_group'] = options.get('source_group') or get_group(GROUP_TYPE.SYSTEM, GROUP_CODE_RADAR)
    options.setdefault('source_type', SOURCE_TYPE_MANUAL)


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
    kwargs.setdefault('from_date', datetime(2000, 1, 1))
    kwargs.setdefault('created_group', group)
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


def create_nationality(**kwargs):
    nationality = Nationality(label='British', **kwargs)
    db.session.add(nationality)
    return nationality


def create_ethnicity(**kwargs):
    ethnicity = Ethnicity(code='A', label='British')
    db.session.add(ethnicity)
    return ethnicity


def create_demographics(patient, **kwargs):
    kwargs.setdefault('first_name', 'JOHN')
    kwargs.setdefault('last_name', 'SMITH')
    kwargs.setdefault('gender', 1)
    kwargs.setdefault('date_of_birth', datetime(1990, 1, 1))
    kwargs.setdefault('nationality', get_nationality(1))
    kwargs.setdefault('ethnicity', get_ethnicity(1))
    set_default_users(kwargs)
    set_default_source(kwargs)

    d = PatientDemographics(
        patient=patient,
        **kwargs
    )
    db.session.add(d)

    return d


def create_patient_number(patient, number_group, number, **kwargs):
    set_default_users(kwargs)
    set_default_source(kwargs)

    n = PatientNumber(
        patient=patient,
        number_group=number_group,
        number=number,
        **kwargs
    )
    db.session.add(n)

    return n


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
    return create_group(GROUP_TYPE.COHORT, code, **kwargs)


def create_hospital(code, **kwargs):
    return create_group(GROUP_TYPE.HOSPITAL, code, **kwargs)


def create_fixtures():
    create_user('admin', is_admin=True)
    create_user('null')

    radar_group = create_group(GROUP_TYPE.SYSTEM, GROUP_CODE_RADAR)
    nhs_group = create_group(GROUP_TYPE.OTHER, GROUP_CODE_NHS, is_recruitment_number_group=True)
    cohort1_group = create_cohort('COHORT1', parent_group=radar_group)
    cohort2_group = create_cohort('COHORT2', parent_group=radar_group)
    hospital1_group = create_hospital('HOSPITAL1')
    hospital2_group = create_hospital('HOSPITAL2')

    hospital_clinician = create_user('hospital_clinician')
    add_user_to_group(hospital_clinician, hospital1_group, ROLE.CLINICIAN)
    add_user_to_group(hospital_clinician, hospital2_group, ROLE.CLINICIAN)

    hospital_senior_clinician = create_user('hospital_senior_clinician')
    add_user_to_group(hospital_senior_clinician, hospital1_group, ROLE.SENIOR_CLINICIAN)
    add_user_to_group(hospital_senior_clinician, hospital2_group, ROLE.SENIOR_CLINICIAN)

    cohort1_researcher = create_user('cohort1_researcher')
    add_user_to_group(cohort1_researcher, cohort1_group, ROLE.RESEARCHER)

    cohort1_senior_researcher = create_user('cohort1_senior_researcher')
    add_user_to_group(cohort1_senior_researcher, cohort1_group, ROLE.SENIOR_RESEARCHER)

    cohort2_researcher = create_user('cohort2_researcher')
    add_user_to_group(cohort2_researcher, cohort2_group, ROLE.RESEARCHER)

    hospital1_clinician = create_user('hospital1_clinician')
    add_user_to_group(hospital1_clinician, hospital1_group, ROLE.CLINICIAN)

    hospital1_senior_clinician = create_user('hospital1_senior_clinician')
    add_user_to_group(hospital1_senior_clinician, hospital1_group, ROLE.SENIOR_CLINICIAN)

    hospital1_admin = create_user('hospital1_admin')
    add_user_to_group(hospital1_admin, hospital1_group, ROLE.ADMIN)

    hospital1_it = create_user('hospital1_it')
    add_user_to_group(hospital1_it, hospital1_group, ROLE.IT)

    hospital2_clinician = create_user('hospital2_clinician')
    add_user_to_group(hospital2_clinician, hospital2_group, ROLE.CLINICIAN)

    create_nationality(id=1)
    create_ethnicity(id=1)

    patient1 = create_patient(id=1)
    add_patient_to_group(patient1, radar_group)
    add_patient_to_group(patient1, cohort1_group)
    add_patient_to_group(patient1, hospital1_group)
    create_demographics(patient1)
    create_patient_number(patient1, nhs_group, '9434765870')

    patient2 = create_patient(id=2)
    add_patient_to_group(patient2, radar_group)
    add_patient_to_group(patient2, cohort1_group)
    add_patient_to_group(patient2, hospital1_group)

    # Set the next patient id
    db.session.execute("SELECT setval('patients_seq', (SELECT MAX(id) FROM patients) + 1)")
