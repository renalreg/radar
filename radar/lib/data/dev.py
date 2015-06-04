import random
from datetime import date, datetime

from radar.lib.data import create_initial_data
from radar.lib.data.utils import random_date, generate_gender, generate_first_name, generate_last_name, \
    generate_date_of_birth, generate_date_of_death, generate_phone_number, generate_mobile_number, \
    generate_email_address, generate_nhs_no, generate_chi_no, random_datetime
from radar.models import LabGroupDefinition, LabResultDefinition, LabGroupResultDefinition, LabGroup, LabResult, \
    DiseaseGroupLabGroupDefinition
from radar.web.app import create_app
from radar.lib.database import db
from radar.models.disease_groups import DiseaseGroup, DiseaseGroupPatient, DiseaseGroupFeature
from radar.models.facilities import Facility
from radar.models.news import Post
from radar.models.patients import Patient, PatientDemographics
from radar.models.units import Unit, UnitPatient
from radar.models.users import User
from jinja2.utils import generate_lorem_ipsum


def create_users(n):
    for x in range(n):
        user = User()
        user.first_name = generate_first_name().capitalize()
        user.last_name = generate_last_name().capitalize()
        user.username = '%s.%s%d' % (
            user.first_name.lower(),
            user.last_name.lower(),
            x + 1
        )
        user.email = '%s@example.org' % user.username
        user.set_password('password')
        db.session.add(user)


def create_admin_user():
    admin = User(username='admin', email='admin@example.org', is_admin=True)
    admin.set_password('password')
    db.session.add(admin)


def create_posts(n):
    for x in range(n):
        d = random_date(date(2008, 1, 1), date.today())

        post = Post()
        post.title = '%s Newsletter' % d.strftime('%b %Y')
        post.body = generate_lorem_ipsum(n=3, html=False)
        post.published = d
        db.session.add(post)


def create_fixtures():
    create_initial_data()

    create_admin_user()
    create_users(10)
    create_posts(10)

    radar_facility = Facility(code='RADAR', name='RADAR', is_internal=True)
    db.session.add(radar_facility)

    group_definition = LabGroupDefinition(code='TEST', name='Example Test', short_name='Example Test', pre_post=True)
    db.session.add(group_definition)

    result1_definition = LabResultDefinition(code='FOO', name='Foo', short_name='Foo', units='foo')
    db.session.add(result1_definition)

    result2_definition = LabResultDefinition(code='BAR', name='Bar', short_name='Bar', units='bar')
    db.session.add(result2_definition)

    result3_definition = LabResultDefinition(code='BAZ', name='Baz', short_name='Baz', units='baz')
    db.session.add(result3_definition)

    group_result1_definition = LabGroupResultDefinition(lab_group_definition=group_definition, lab_result_definition=result1_definition, weight=1)
    db.session.add(group_result1_definition)

    group_result2_definition = LabGroupResultDefinition(lab_group_definition=group_definition, lab_result_definition=result2_definition, weight=2)
    db.session.add(group_result2_definition)

    group_result3_definition = LabGroupResultDefinition(lab_group_definition=group_definition, lab_result_definition=result3_definition, weight=3)
    db.session.add(group_result3_definition)

    # http://en.wikipedia.org/wiki/List_of_fictional_institutions#Hospitals
    units = [
        Unit(name='All Saints Hospital'),
        Unit(name='Chelsea General Hospital'),
        Unit(name='Chicago Hope'),
        Unit(name='County General Hospital'),
        Unit(name='Community General Hospital'),
    ]

    for unit in units:
        db.session.add(unit)

    facilities = [
        Facility(code='A', name='All Saints Hospital', unit=units[0], is_internal=True),
        Facility(code='B', name='Chelsea General Hospital', unit=units[1], is_internal=True),
        Facility(code='C', name='Chicago Hope', unit=units[2], is_internal=True),
        Facility(code='D', name='County General Hospital', unit=units[3], is_internal=True),
        Facility(code='E', name='Community General Hospital', unit=units[4], is_internal=True),
    ]

    for facility in facilities:
        db.session.add(facility)

    disease_groups = [
        DiseaseGroup(
            name='SRNS',
            features=[
                DiseaseGroupFeature(name='DEMOGRAPHICS', weight=0),
                DiseaseGroupFeature(name='GENETICS', weight=1),
                DiseaseGroupFeature(name='RENAL_IMAGING', weight=2),
                DiseaseGroupFeature(name='SALT_WASTING_CLINICAL_FEATURES', weight=3)
            ],
            disease_group_lab_group_definitions=[
                DiseaseGroupLabGroupDefinition(lab_group_definition=group_definition, weight=4)
            ]
        ),
        DiseaseGroup(
            name='MPGN',
            features=[
                DiseaseGroupFeature(name='DEMOGRAPHICS', weight=0),
                DiseaseGroupFeature(name='GENETICS', weight=3),
                DiseaseGroupFeature(name='RENAL_IMAGING', weight=2),
                DiseaseGroupFeature(name='SALT_WASTING_CLINICAL_FEATURES', weight=1)
            ],
            disease_group_lab_group_definitions=[
                DiseaseGroupLabGroupDefinition(lab_group_definition=group_definition, weight=4)
            ]
        ),
        DiseaseGroup(
            name='Salt Wasting',
            features=[
                DiseaseGroupFeature(name='DEMOGRAPHICS', weight=0),
                DiseaseGroupFeature(name='GENETICS', weight=0),
                DiseaseGroupFeature(name='RENAL_IMAGING', weight=0),
                DiseaseGroupFeature(name='SALT_WASTING_CLINICAL_FEATURES', weight=0)
            ],
            disease_group_lab_group_definitions=[
                DiseaseGroupLabGroupDefinition(lab_group_definition=group_definition, weight=4)
            ]
        ),
    ]

    for disease_group in disease_groups:
        db.session.add(disease_group)

    for _ in range(100):
        patient = Patient()
        patient.recruited_date = random_date(date(2008, 1, 1), date.today())

        for facility in random.sample(facilities, random.randint(1, 3)):
            unit_patient = UnitPatient(unit=facility.unit, patient=patient)
            unit_patient.created_date = random_date(patient.recruited_date, date.today())
            db.session.add(unit_patient)

            gender = generate_gender()
            d = PatientDemographics()
            d.patient = patient
            d.facility = facility
            d.first_name = generate_first_name(gender)
            d.last_name = generate_last_name()
            d.gender = gender
            d.date_of_birth = generate_date_of_birth()

            # 10% chance of being dead :(
            if random.random() < 0.1:
                d.date_of_death = generate_date_of_death()

            d.home_number = generate_phone_number()
            d.mobile_number = generate_mobile_number()
            d.work_number = generate_phone_number()
            d.email_address = generate_email_address(d.first_name, d.last_name)

            r = random.random()

            if r > 0.9:
                d.nhs_no = generate_nhs_no()
                d.chi_no = generate_chi_no()
            elif r > 0.8:
                d.chi_no = generate_chi_no()
            elif r > 0.1:
                d.nhs_no = generate_nhs_no()

            db.session.add(d)

            for x in range(10):
                test_group = LabGroup(
                    patient=patient,
                    facility=facility,
                    lab_group_definition=group_definition,
                    date=random_datetime(datetime(2000, 1, 1), datetime.now()),
                    pre_post='pre'
                )
                test_group.lab_results = [
                    LabResult(lab_group=test_group, lab_result_definition=result1_definition, value=random.randint(1, 100)),
                    LabResult(lab_group=test_group, lab_result_definition=result2_definition, value=random.randint(1, 100)),
                    LabResult(lab_group=test_group, lab_result_definition=result3_definition, value=random.randint(1, 100)),
                ]
                db.session.add(test_group)

        disease_group = random.choice(disease_groups)
        disease_group_patient = DiseaseGroupPatient(disease_group=disease_group, patient=patient)
        disease_group_patient.created_date = random_date(patient.recruited_date, date.today())
        db.session.add(disease_group_patient)

        db.session.add(patient)


if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        create_fixtures()
