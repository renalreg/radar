import random
from datetime import date, timedelta, datetime

from radar.lib.data import create_initial_data
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


FEMALE = 'F'
MALE = 'M'

FIRST_NAMES = {
    MALE: [
        'JACK',
        'JOSHUA',
        'THOMAS',
        'JAMES',
        'OLIVER',
        'DANIEL',
        'SAMUEL',
        'WILLIAM',
        'HARRY',
        'JOSEPH',
        'BENJAMIN',
        'CHARLIE',
        'LUKE',
        'CALLUM',
        'MATTHEW',
        'JAKE',
        'GEORGE',
        'ETHAN',
        'LEWIS',
        'MOHAMMED',
        'JACOB',
        'ALEXANDER',
        'ALFIE',
        'DYLAN',
        'RYAN',
    ],
    FEMALE: [
        'JESSICA',
        'EMILY',
        'SOPHIE',
        'OLIVIA',
        'ELLIE',
        'CHLOE',
        'GRACE',
        'LUCY',
        'CHARLOTTE',
        'ELLA',
        'KATIE',
        'RUBY',
        'MEGAN',
        'HANNAH',
        'AMELIA',
        'LILY',
        'AMY',
        'MIA',
        'HOLLY',
        'ABIGAIL',
        'MILLIE',
        'MOLLY',
        'EMMA',
        'ISABELLA',
        'LEAH',
    ]
}

LAST_NAMES = [
    'SMITH',
    'JONES',
    'TAYLOR',
    'WILLIAMS',
    'BROWN',
    'DAVIES',
    'EVANS',
    'WILSON',
    'THOMAS',
    'ROBERTS',
    'JOHNSON',
    'LEWIS',
    'WALKER',
    'ROBINSON',
    'WOOD',
    'THOMPSON',
    'WHITE',
    'WATSON',
    'JACKSON',
    'WRIGHT',
    'GREEN',
    'HARRIS',
    'COOPER',
    'KING',
    'LEE',
]


def generate_gender():
    if random.random() > 0.5:
        return MALE
    else:
        return FEMALE


def generate_first_name(gender):
    return random.choice(FIRST_NAMES[gender])


def generate_last_name():
    return random.choice(LAST_NAMES)


def generate_date_of_birth():
    return random_date(date(1920, 1, 1), date(2000, 12, 31))


def generate_date_of_death():
    return random_date(date(1980, 1, 1), date(2014, 12, 31))


def random_date(start_date, end_date):
    if start_date == end_date:
        return start_date

    days = (end_date - start_date).days
    random_date = start_date + timedelta(days=random.randint(1, days))
    return random_date


def random_bool():
    return random.randint(0, 1) == 1


def random_datetime(start_dt, end_dt):
    seconds = int((end_dt - start_dt).total_seconds())
    return start_dt + timedelta(seconds=random.randrange(seconds))


def generate_email_address(first_name, last_name):
    return '%s.%s@example.org' % (first_name.lower(), last_name.lower())


def generate_phone_number():
    return '0%d%s %s' % (
        random.randint(1, 2),
        ''.join(str(random.randint(0, 9)) for _ in range(3)),
        ''.join(str(random.randint(0, 9)) for _ in range(6)),
    )


def generate_mobile_number():
    return '07' + ''.join(str(random.randint(0, 9)) for _ in range(9))


def generate_nhs_no():
    while True:
        number = ''.join(str(random.randint(0, 9)) for _ in range(9))

        check_digit = 0

        for i in range(9):
            check_digit += int(number[i]) * (10 - i)

        check_digit = 11 - (check_digit % 11)

        if check_digit == 11:
            check_digit = 0
        elif check_digit == 10:
            continue

        number += str(check_digit)

        return int(number)


def generate_chi_no():
    return generate_nhs_no()


def create_fixtures():
    create_initial_data()

    admin = User(username='admin', email='admin@example.org', is_admin=True)
    admin.set_password('password')
    db.session.add(admin)

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

    post = Post()
    post.title = 'Hello'
    post.body = 'Hello World!'
    post.published = datetime.now()
    db.session.add(post)


if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        create_fixtures()
