import random
from datetime import date, datetime

from jinja2.utils import generate_lorem_ipsum
from sqlalchemy import func

from radar.lib.data import create_initial_data
from radar.lib.data.dev_constants import MEDICATION_NAMES
from radar.lib.data.dev_utils import random_date, generate_gender, generate_first_name, generate_last_name, \
    generate_date_of_birth, generate_date_of_death, generate_phone_number, generate_mobile_number, \
    generate_email_address, generate_nhs_no, generate_chi_no, random_datetime, random_bool
from radar.lib.data.validation import validate_user, validate_post, validate_patient_demographics, validate_dialysis, \
    validate_medication, validate_transplant, validate_hospitalisation, validate_plasmapheresis, validate_renal_imaging, \
    validate_patient, validate_organisation_patient, validate_cohort_patient, validate_result_group
from radar.lib.data_sources import get_radar_data_source
from radar.lib.models import DialysisType, Dialysis, Medication, Transplant, Hospitalisation, Plasmapheresis,\
    RenalImaging, Result, ResultGroup, ResultGroupDefinition, EthnicityCode, MEDICATION_DOSE_UNITS, \
    MEDICATION_FREQUENCIES, MEDICATION_ROUTES, TRANSPLANT_TYPES, PLASMAPHERESIS_RESPONSES, RENAL_IMAGING_TYPES, \
    RENAL_IMAGING_KIDNEY_TYPES, ORGANISATION_TYPE_UNIT, Organisation, DataSource, OrganisationPatient, CohortPatient, \
    PLASMAPHERESIS_NO_OF_EXCHANGES
from radar.lib.database import db
from radar.lib.models.cohorts import Cohort
from radar.lib.models.posts import Post
from radar.lib.models.patients import Patient, PatientDemographics
from radar.lib.models.users import User


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
        user.password = 'password'
        user = validate_user(user)
        db.session.add(user)


def create_admin_user():
    admin = User()
    admin.username = 'admin'
    admin.email = 'admin@example.org'
    admin.is_admin = True
    admin.password = 'password'
    admin.created_user = admin
    admin.modified_user = admin
    admin.created_date = func.now()
    admin.modified_date = func.now()
    db.session.add(admin)


def create_posts(n):
    for x in range(n):
        d = random_date(date(2008, 1, 1), date.today())

        post = Post()
        post.title = '%s Newsletter' % d.strftime('%b %Y')
        post.body = generate_lorem_ipsum(n=3, html=False)
        post.published_date = d
        post = validate_post(post)
        db.session.add(post)


def create_result_groups_f():
    result_group_definitions = ResultGroupDefinition.query.all()

    def f(patient, data_source, n):
        for result_group_definition in result_group_definitions:
            for _ in range(n):
                result_group = ResultGroup()
                result_group.patient = patient
                result_group.data_source = data_source
                result_group.result_group_definition = result_group_definition
                result_group.date = random_datetime(datetime(2000, 1, 1), datetime.now())

                if result_group_definition.pre_post:
                    result_group.pre_post = 'pre'  # TODO random

                result_group = validate_result_group(result_group)

                db.session.add(result_group)

                for result_definition in result_group_definition.result_definitions:
                    result = Result(
                        result_group=result_group,
                        result_definition=result_definition,
                        value=random.randint(1, 100),  # TODO use min max
                    )
                    db.session.add(result)

    return f


def create_demographics_f():
    ethnicity_codes = EthnicityCode.query.all()

    def f(patient, data_source, gender):
        d = PatientDemographics()
        d.patient = patient
        d.data_source = data_source
        d.first_name = generate_first_name(gender)
        d.last_name = generate_last_name()
        d.gender = gender
        d.date_of_birth = generate_date_of_birth()
        d.ethnicity_code = random.choice(ethnicity_codes)

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

        d = validate_patient_demographics(d)

        db.session.add(d)

    return f


def create_dialysis_f():
    dialysis_types = DialysisType.query.all()

    def f(patient, data_source, n):
        for _ in range(n):
            dialysis = Dialysis()
            dialysis.patient = patient
            dialysis.data_source = data_source
            dialysis.from_date = random_date(date(2000, 1, 1), date.today())

            if random.random() > 0.5:
                dialysis.to_date = random_date(dialysis.from_date, date.today())

            dialysis.dialysis_type = random.choice(dialysis_types)

            dialysis = validate_dialysis(dialysis)

            db.session.add(dialysis)

    return f


def create_medications_f():
    def f(patient, data_source, n):
        for _ in range(n):
            medication = Medication()
            medication.patient = patient
            medication.data_source = data_source
            medication.from_date = random_date(date(2000, 1, 1), date.today())

            if random.random() > 0.5:
                medication.to_date = random_date(medication.from_date, date.today())

            medication.name = random.choice(MEDICATION_NAMES)
            medication.dose_quantity = random.randint(1, 10)
            medication.dose_unit = random.choice(MEDICATION_DOSE_UNITS.keys())
            medication.frequency = random.choice(MEDICATION_FREQUENCIES.keys())
            medication.route = random.choice(MEDICATION_ROUTES.keys())

            medication = validate_medication(medication)

            db.session.add(medication)

    return f


def create_transplants_f():
    def f(patient, data_source, n):
        for _ in range(n):
            transplant = Transplant()
            transplant.patient = patient
            transplant.data_source = data_source
            transplant.transplant_date = random_date(date(2000, 1, 1), date.today())
            transplant.transplant_type = random.choice(TRANSPLANT_TYPES.keys())
            transplant.recurred = random_bool()

            if transplant.recurred:
                transplant.date_recurred = random_date(transplant.transplant_date, date.today())

            if random.random() > 0.75:
                transplant.date_failed = random_date(transplant.transplant_date, date.today())

            transplant = validate_transplant(transplant)

            db.session.add(transplant)

    return f


def create_hospitalisations_f():
    def f(patient, data_source, n):
        for _ in range(n):
            hospitalisation = Hospitalisation()
            hospitalisation.patient = patient
            hospitalisation.data_source = data_source
            hospitalisation.date_of_admission = random_date(date(2000, 1, 1), date.today())
            hospitalisation.date_of_discharge = random_date(hospitalisation.date_of_admission, date.today())
            hospitalisation.reason_for_admission = 'Test'

            hospitalisation = validate_hospitalisation(hospitalisation)

            db.session.add(hospitalisation)

    return f


def create_plasmapheresis_f():
    def f(patient, data_source, n):
        for _ in range(n):
            plasmapheresis = Plasmapheresis()
            plasmapheresis.patient = patient
            plasmapheresis.data_source = data_source
            plasmapheresis.from_date = random_date(date(2000, 1, 1), date.today())

            if random.random() > 0.5:
                plasmapheresis.to_date = random_date(plasmapheresis.from_date, date.today())

            plasmapheresis.no_of_exchanges = random.choice(PLASMAPHERESIS_NO_OF_EXCHANGES.keys())
            plasmapheresis.response = random.choice(PLASMAPHERESIS_RESPONSES.keys())

            plasmapheresis = validate_plasmapheresis(plasmapheresis)

            db.session.add(plasmapheresis)

    return f


def create_renal_imaging_f():
    def f(patient, data_source, n):
        for _ in range(n):
            renal_imaging = RenalImaging()
            renal_imaging.patient = patient
            renal_imaging.data_source = data_source
            renal_imaging.date = random_date(date(2000, 1, 1), date.today())
            renal_imaging.imaging_type = random.choice(RENAL_IMAGING_TYPES.keys())
            renal_imaging.right_present = random_bool()
            renal_imaging.left_present = random_bool()

            if renal_imaging.right_present:
                renal_imaging.right_type = random.choice(RENAL_IMAGING_KIDNEY_TYPES.keys())
                renal_imaging.right_length = random.randint(11, 14)
                renal_imaging.right_cysts = random_bool()
                renal_imaging.right_calcification = random_bool()

                if renal_imaging.right_calcification:
                    renal_imaging.right_nephrocalcinosis = random_bool()
                    renal_imaging.right_nephrolithiasis = random_bool()

            if renal_imaging.left_present:
                renal_imaging.left_type = random.choice(RENAL_IMAGING_KIDNEY_TYPES.keys())
                renal_imaging.left_length = random.randint(11, 14)
                renal_imaging.left_cysts = random_bool()
                renal_imaging.left_calcification = random_bool()

                if renal_imaging.left_calcification:
                    renal_imaging.left_nephrocalcinosis = random_bool()
                    renal_imaging.left_nephrolithiasis = random_bool()

            renal_imaging = validate_renal_imaging(renal_imaging)

            db.session.add(renal_imaging)

    return f


def create_patients(n):
    radar_data_source = get_radar_data_source()
    data_sources = DataSource.query\
        .join(DataSource.organisation)\
        .filter(Organisation.type == ORGANISATION_TYPE_UNIT)\
        .all()
    cohorts = Cohort.query.all()

    create_demographics = create_demographics_f()
    create_dialysis = create_dialysis_f()
    create_medications = create_medications_f()
    create_transplants = create_transplants_f()
    create_plasmapheresis = create_plasmapheresis_f()
    create_hospitalisations = create_hospitalisations_f()
    create_renal_imaging = create_renal_imaging_f()
    create_result_groups = create_result_groups_f()

    for _ in range(n):
        patient = Patient()
        patient.recruited_date = random_date(date(2008, 1, 1), date.today())

        patient = validate_patient(patient)

        db.session.add(patient)

        gender = generate_gender()

        create_demographics(patient, radar_data_source, gender)

        for data_source in random.sample(data_sources, random.randint(1, 3)):
            organisation_patient = OrganisationPatient()
            organisation_patient.organisation = data_source.organisation
            organisation_patient.patient = patient
            organisation_patient.created_date = random_date(patient.recruited_date, date.today())
            organisation_patient = validate_organisation_patient(organisation_patient)
            db.session.add(organisation_patient)

            create_demographics(patient, data_source, gender)
            create_result_groups(patient, data_source, 10)
            create_dialysis(patient, data_source, 5)
            create_medications(patient, data_source, 5)
            create_transplants(patient, data_source, 3)
            create_hospitalisations(patient, data_source, 3)
            create_plasmapheresis(patient, data_source, 3)
            create_renal_imaging(patient, data_source, 3)

        cohort_patient = CohortPatient()
        cohort_patient.cohort = random.choice(cohorts)
        cohort_patient.patient = patient
        cohort_patient.created_date = random_date(patient.recruited_date, date.today())
        cohort_patient = validate_cohort_patient(cohort_patient)
        db.session.add(cohort_patient)


def create_data(patients_n):
    # Always generate the same "random" data
    random.seed(0)

    create_admin_user()

    create_initial_data()

    create_users(10)
    create_posts(10)
    create_patients(patients_n)
