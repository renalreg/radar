import random
from datetime import date, datetime

from jinja2.utils import generate_lorem_ipsum

from radar.lib.data import create_initial_data
from radar.lib.data.dev_constants import MEDICATION_NAMES
from radar.lib.data.dev_utils import random_date, generate_gender, generate_first_name, generate_last_name, \
    generate_date_of_birth, generate_date_of_death, generate_phone_number, generate_mobile_number, \
    generate_email_address, generate_nhs_no, generate_chi_no, random_datetime
from radar.lib.facilities import get_radar_facility
from radar.models import LabGroupDefinition, LabGroup, LabResult, DialysisType, Dialysis, Medication, MedicationRoute, \
    MedicationFrequency, MedicationDoseUnit
from radar.web.app import create_app
from radar.lib.database import db
from radar.models.disease_groups import DiseaseGroup, DiseaseGroupPatient
from radar.models.facilities import Facility
from radar.models.news import Post
from radar.models.patients import Patient, PatientDemographics
from radar.models.units import UnitPatient
from radar.models.users import User


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


def create_lab_groups(patient, facility, lab_group_definitions, n):
    for lab_group_definition in lab_group_definitions:
        for _ in range(n):
            lab_group = LabGroup(
                patient=patient,
                facility=facility,
                lab_group_definition=lab_group_definition,
                date=random_datetime(datetime(2000, 1, 1), datetime.now()),
            )

            if lab_group_definition.pre_post:
                lab_group.pre_post = 'pre'  # TODO random

            db.session.add(lab_group)

            for lab_result_definition in lab_group_definition.lab_result_definitions:
                lab_result = LabResult(
                    lab_group=lab_group,
                    lab_result_definition=lab_result_definition,
                    value=random.randint(1, 100),  # TODO use min max
                )
                db.session.add(lab_result)


def create_demographics(patient, facility, gender):
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


def create_dialysis_f():
    dialysis_types = DialysisType.query.all()

    def f(patient, facility, n):
        for _ in range(n):
            dialysis = Dialysis()
            dialysis.patient = patient
            dialysis.facility = facility
            dialysis.from_date = random_date(patient.recruited_date, date.today())

            if random.random() > 0.5:
                dialysis.to_date = random_date(dialysis.from_date, date.today())

            dialysis.dialysis_type = random.choice(dialysis_types)
            db.session.add(dialysis)

    return f


def create_medications_f():
    medication_routes = MedicationRoute.query.all()
    medication_frequencies = MedicationFrequency.query.all()
    medication_dose_units = MedicationDoseUnit.query.all()

    def f(patient, facility, n):
        for _ in range(n):
            medication = Medication()
            medication.patient = patient
            medication.facility = facility
            medication.from_date = random_date(patient.recruited_date, date.today())

            if random.random() > 0.5:
                medication.to_date = random_date(medication.from_date, date.today())

            medication.name = random.choice(MEDICATION_NAMES)
            medication.dose_quantity = random.randint(1, 10)
            medication.dose_unit = random.choice(medication_dose_units)
            medication.frequency = random.choice(medication_frequencies)
            medication.route = random.choice(medication_routes)
            db.session.add(medication)

    return f


def create_patients(n):
    # TODO create data for remote facilities

    radar_facility = get_radar_facility()
    unit_facilities = Facility.query\
        .join(Facility.unit)\
        .filter(Facility.is_internal)\
        .all()
    disease_groups = DiseaseGroup.query.all()
    lab_group_definitions = LabGroupDefinition.query.all()

    create_dialysis = create_dialysis_f()
    create_medications = create_medications_f()

    for _ in range(n):
        patient = Patient()
        patient.recruited_date = random_date(date(2008, 1, 1), date.today())
        db.session.add(patient)

        gender = generate_gender()

        create_demographics(patient, radar_facility, gender)

        for facility in random.sample(unit_facilities, random.randint(1, 3)):
            unit_patient = UnitPatient(unit=facility.unit, patient=patient)
            unit_patient.created_date = random_date(patient.recruited_date, date.today())
            db.session.add(unit_patient)

            create_demographics(patient, facility, gender)
            create_lab_groups(patient, facility, lab_group_definitions, 10)
            create_dialysis(patient, facility, 5)
            create_medications(patient, facility, 5)

        disease_group = random.choice(disease_groups)
        disease_group_patient = DiseaseGroupPatient(disease_group=disease_group, patient=patient)
        disease_group_patient.created_date = random_date(patient.recruited_date, date.today())
        db.session.add(disease_group_patient)


def create_data(patients_n):
    # Always generate the same "random" data
    random.seed(0)

    create_initial_data()

    create_admin_user()
    create_users(10)
    create_posts(10)
    create_patients(patients_n)


if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        create_data(1)
