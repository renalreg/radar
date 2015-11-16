import random
from datetime import date, datetime, timedelta

from jinja2.utils import generate_lorem_ipsum
import pytz
from sqlalchemy import func, desc

from radar.fixtures import create_initial_data
from radar.fixtures.dev.constants import MEDICATION_NAMES
from radar.fixtures.dev.utils import random_date, generate_gender, generate_first_name, generate_last_name, \
    generate_date_of_birth, generate_date_of_death, generate_phone_number, generate_mobile_number, \
    generate_email_address, random_datetime, random_bool, generate_first_name_alias, generate_nhsbt_no, generate_ukrr_no, \
    generate_chi_no, generate_nhs_no, generate_address_line_1, generate_address_line_2, generate_address_line_3, \
    generate_postcode
from radar.fixtures.validation import validate_and_add
from radar.data_sources import get_radar_data_source, DATA_SOURCE_TYPE_RADAR
from radar.models import DialysisType, Dialysis, Medication, Transplant, Hospitalisation, Plasmapheresis,\
    RenalImaging, ResultGroup, EthnicityCode, MEDICATION_DOSE_UNITS, \
    MEDICATION_FREQUENCIES, MEDICATION_ROUTES, TRANSPLANT_TYPES, PLASMAPHERESIS_RESPONSES, RENAL_IMAGING_TYPES, \
    RENAL_IMAGING_KIDNEY_TYPES, ORGANISATION_TYPE_UNIT, Organisation, OrganisationPatient, CohortPatient, \
    PLASMAPHERESIS_NO_OF_EXCHANGES, OrganisationUser, PatientAlias, PatientNumber, PatientAddress, CohortUser, \
    ResultGroupSpec, RESULT_SPEC_TYPE_INTEGER, RESULT_SPEC_TYPE_FLOAT, RESULT_SPEC_TYPE_CODED_INTEGER, \
    RESULT_SPEC_TYPE_CODED_STRING
from radar.database import db
from radar.models.cohorts import Cohort
from radar.models.posts import Post
from radar.models.patients import Patient, PatientDemographics, GENDER_FEMALE
from radar.models.users import User
from radar.organisations import get_nhs_organisation, get_chi_organisation, get_ukrr_organisation, \
    get_nhsbt_organisation, get_radar_organisation
from radar.roles import ORGANISATION_SENIOR_CLINICIAN, COHORT_RESEARCHER, COHORT_SENIOR_RESEARCHER
from radar.cohorts import get_radar_cohort


PASSWORD = 'password'


def create_users(n):
    for x in range(n):
        username = 'user%d' % (x + 1)

        if User.query.filter(User.username == username).first() is not None:
            continue

        user = User()
        user.first_name = generate_first_name(generate_gender()).capitalize()
        user.last_name = generate_last_name().capitalize()
        user.username = username
        user.email = '%s@example.org' % username
        user.password = PASSWORD
        user.is_admin = True
        validate_and_add(user, {'allow_weak_passwords': True})


def create_admin_user():
    user = User()
    user.username = 'admin'
    user.email = 'admin@example.org'
    user.first_name = 'Foo'
    user.last_name = 'Bar'
    user.is_admin = True
    user.password = PASSWORD
    validate_and_add(user, {'allow_weak_passwords': True})


def create_bot_user():
    bot = User()
    bot.username = 'bot'
    bot.email = 'bot@example.org'
    bot.is_admin = True
    bot.is_bot = True
    bot.password = PASSWORD
    bot.created_user = bot
    bot.modified_user = bot
    bot.created_date = func.now()
    bot.modified_date = func.now()
    db.session.add(bot)
    db.session.flush()


def create_southmead_user():
    user = User()
    user.username = 'southmead_demo'
    user.email = 'southmead_demo@example.org'
    user.first_name = 'Foo'
    user.last_name = 'Bar'
    user.is_admin = False
    user.password = PASSWORD
    user = validate_and_add(user, {'allow_weak_passwords': True})

    organisation_user = OrganisationUser()
    organisation_user.user = user
    organisation_user.organisation = Organisation.query.filter(Organisation.code == 'REE01').one()
    organisation_user.role = ORGANISATION_SENIOR_CLINICIAN
    validate_and_add(organisation_user)


def create_srns_user():
    user = User()
    user.username = 'srns_demo'
    user.email = 'srns_demo@example.org'
    user.first_name = 'Foo'
    user.last_name = 'Bar'
    user.is_admin = False
    user.password = PASSWORD
    user = validate_and_add(user, {'allow_weak_passwords': True})

    cohort_user = CohortUser()
    cohort_user.user = user
    cohort_user.cohort = Cohort.query.filter(Cohort.code == 'INS').one()
    cohort_user.role = COHORT_RESEARCHER
    validate_and_add(cohort_user)


def create_srns_demograhics_user():
    user = User()
    user.username = 'srns_demographics_demo'
    user.email = 'srns_demographics_demo@example.org'
    user.first_name = 'Foo'
    user.last_name = 'Bar'
    user.is_admin = False
    user.password = PASSWORD
    user = validate_and_add(user, {'allow_weak_passwords': True})

    cohort_user = CohortUser()
    cohort_user.user = user
    cohort_user.cohort = Cohort.query.filter(Cohort.code == 'INS').one()
    cohort_user.role = COHORT_SENIOR_RESEARCHER
    validate_and_add(cohort_user)


def create_posts(n):
    for x in range(n):
        d = random_date(date(2008, 1, 1), date.today() - timedelta(days=1))

        post = Post()
        post.title = '%s Newsletter' % d.strftime('%b %Y')
        post.body = generate_lorem_ipsum(n=3, html=False)
        post.published_date = d
        validate_and_add(post)

    post = Post()
    post.title = 'New RaDaR Conditions'
    post.body = 'RaDaR is now open to two new conditions - Calciphylaxis and IgA Nephropathy. '\
        'No new approvals are needed for these conditions and patients are registered in the normal fashion.'
    post.published_date = date.today()
    validate_and_add(post)


def create_result_groups_f():
    result_group_specs = ResultGroupSpec.query.all()

    def f(patient, data_source, n):
        for result_group_spec in result_group_specs:
            for _ in range(n):
                result_group = ResultGroup()
                result_group.patient = patient
                result_group.data_source = data_source
                result_group.result_group_spec = result_group_spec
                result_group.date = random_datetime(patient.earliest_date_of_birth, datetime.now(pytz.utc))

                result_group.results = results = {}

                for result_spec in result_group_spec.result_specs:
                    type = result_spec.type

                    if type == RESULT_SPEC_TYPE_INTEGER or type == RESULT_SPEC_TYPE_FLOAT:
                        min_value = result_spec.min_value or 0
                        max_value = result_spec.max_value or 100
                        results[result_spec.code] = random.randint(min_value, max_value)
                    elif type == RESULT_SPEC_TYPE_CODED_STRING or type == RESULT_SPEC_TYPE_CODED_INTEGER:
                        results[result_spec.code] = random.choice(result_spec.option_values)

                validate_and_add(result_group)

    return f


def create_demographics_f():
    ethnicity_codes = EthnicityCode.query.all()

    def create_demographics(patient, data_source, gender):
        old_d = PatientDemographics.query.filter(PatientDemographics.patient == patient).first()
        new_d = PatientDemographics()
        new_d.patient = patient
        new_d.data_source = data_source

        if old_d is None:
            new_d.first_name = generate_first_name(gender)
            new_d.last_name = generate_last_name()
            new_d.gender = gender
            new_d.date_of_birth = generate_date_of_birth()
            new_d.ethnicity_code = random.choice(ethnicity_codes)

            # 10% chance of being dead :(
            if random.random() < 0.1:
                new_d.date_of_death = generate_date_of_death(new_d.date_of_birth)

            new_d.home_number = generate_phone_number()
            new_d.mobile_number = generate_mobile_number()
            new_d.work_number = generate_phone_number()
            new_d.email_address = generate_email_address(new_d.first_name, new_d.last_name)
        else:
            # 50% chance of mutating the first name
            if random.random() > 0.5:
                new_d.first_name = generate_first_name_alias(old_d.gender, old_d.first_name)
            else:
                new_d.first_name = old_d.first_name

            # Maiden name
            if new_d.gender == GENDER_FEMALE and random.random() > 0.5:
                new_d.last_name = generate_last_name()
            else:
                new_d.last_name = old_d.last_name

            new_d.gender = old_d.gender
            new_d.date_of_birth = old_d.date_of_birth

            # 50% chance of the DOB being incorrect
            if random.random() > 0.5:
                new_d.date_of_birth = new_d.date_of_birth + timedelta(random.randint(-100, 100))

            new_d.ethnicity_code = old_d.ethnicity_code
            new_d.date_of_death = old_d.date_of_death
            new_d.home_number = old_d.home_number
            new_d.mobile_number = old_d.mobile_number
            new_d.work_number = old_d.work_number
            new_d.email_address = old_d.email_address

        validate_and_add(new_d)

    return create_demographics


def create_patient_aliases_f():
    def create_patient_aliases(patient, data_source):
        d = PatientDemographics.query.filter(PatientDemographics.patient == patient).first()

        alias = PatientAlias()
        alias.patient = patient
        alias.data_source = data_source

        # 50% chance of mutating the first name
        if random.random() > 0.5:
            alias.first_name = generate_first_name_alias(d.gender, d.first_name)
        else:
            alias.first_name = d.first_name

        # Maiden name
        if d.gender == GENDER_FEMALE and random.random() > 0.5:
            alias.last_name = generate_last_name()
        else:
            alias.last_name = d.last_name

        validate_and_add(alias)

    return create_patient_aliases


def create_patient_numbers_f():
    nhs_organisation = get_nhs_organisation()
    chi_organisation = get_chi_organisation()
    ukrr_organisation = get_ukrr_organisation()
    nhsbt_organisation = get_nhsbt_organisation()

    organisations = [
        (nhs_organisation, generate_nhs_no),
        (chi_organisation, generate_chi_no),
        (ukrr_organisation, generate_ukrr_no),
        (nhsbt_organisation, generate_nhsbt_no),
    ]

    def create_patient_numbers(patient, data_source):
        for organisation, f in organisations:
            old_n = PatientNumber.query.filter(PatientNumber.patient == patient, PatientNumber.organisation == organisation).first()
            new_n = PatientNumber()
            new_n.patient = patient
            new_n.data_source = data_source
            new_n.organisation = organisation

            if old_n is None:
                new_n.number = f()
            else:
                new_n.number = old_n.number

            validate_and_add(new_n)

    return create_patient_numbers


def create_patient_addresses_f():
    def create_patient_addresses(patient, data_source):
        old_a = PatientAddress.query\
            .filter(PatientAddress.patient == patient)\
            .order_by(desc(PatientAddress.from_date), desc(PatientAddress.to_date))\
            .first()

        new_a = PatientAddress()
        new_a.patient = patient
        new_a.data_source = data_source

        if old_a is None:
            new_a.from_date = patient.earliest_date_of_birth
            new_a.address_line_1 = generate_address_line_1()
            new_a.address_line_2 = generate_address_line_2()
            new_a.address_line_3 = generate_address_line_3()
            new_a.postcode = generate_postcode()
        else:
            to_date = random_date(old_a.from_date, date.today())

            if random.random() > 0.5 and to_date != old_a.from_date:
                old_a.to_date = to_date
                new_a.from_date = to_date
                new_a.address_line_1 = generate_address_line_1()
                new_a.address_line_2 = generate_address_line_2()
                new_a.address_line_3 = generate_address_line_3()
                new_a.postcode = generate_postcode()
            else:
                new_a.from_date = old_a.from_date
                new_a.address_line_1 = old_a.address_line_1
                new_a.address_line_2 = old_a.address_line_2
                new_a.address_line_3 = old_a.address_line_3
                new_a.postcode = old_a.postcode

        validate_and_add(new_a)

    return create_patient_addresses


def create_dialysis_f():
    dialysis_types = DialysisType.query.all()

    def create_dialysis(patient, data_source, n):
        for _ in range(n):
            dialysis = Dialysis()
            dialysis.patient = patient
            dialysis.data_source = data_source
            dialysis.from_date = random_date(patient.earliest_date_of_birth, date.today())

            if random.random() > 0.5:
                dialysis.to_date = random_date(dialysis.from_date, date.today())

            dialysis.dialysis_type = random.choice(dialysis_types)

            validate_and_add(dialysis)

    return create_dialysis


def create_medications_f():
    def create_medications(patient, data_source, n):
        for _ in range(n):
            medication = Medication()
            medication.patient = patient
            medication.data_source = data_source
            medication.from_date = random_date(patient.earliest_date_of_birth, date.today())

            if random.random() > 0.5:
                medication.to_date = random_date(medication.from_date, date.today())

            medication.name = random.choice(MEDICATION_NAMES)
            medication.dose_quantity = random.randint(1, 10)
            medication.dose_unit = random.choice(MEDICATION_DOSE_UNITS.keys())
            medication.frequency = random.choice(MEDICATION_FREQUENCIES.keys())
            medication.route = random.choice(MEDICATION_ROUTES.keys())

            validate_and_add(medication)

    return create_medications


def create_transplants_f():
    def create_transplants(patient, data_source, n):
        for _ in range(n):
            transplant = Transplant()
            transplant.patient = patient
            transplant.data_source = data_source
            transplant.transplant_date = random_date(patient.earliest_date_of_birth, date.today())
            transplant.transplant_type = random.choice(TRANSPLANT_TYPES.keys())
            transplant.recurred = random_bool()

            if transplant.recurred:
                transplant.date_recurred = random_date(transplant.transplant_date, date.today())

            if random.random() > 0.75:
                transplant.date_failed = random_date(transplant.transplant_date, date.today())

            validate_and_add(transplant)

    return create_transplants


def create_hospitalisations_f():
    def create_hospitalisations(patient, data_source, n):
        for _ in range(n):
            hospitalisation = Hospitalisation()
            hospitalisation.patient = patient
            hospitalisation.data_source = data_source
            hospitalisation.date_of_admission = random_date(patient.earliest_date_of_birth, date.today())
            hospitalisation.date_of_discharge = random_date(hospitalisation.date_of_admission, date.today())
            hospitalisation.reason_for_admission = 'Test'

            validate_and_add(hospitalisation)

    return create_hospitalisations


def create_plasmapheresis_f():
    def create_plasmapheresis(patient, data_source, n):
        for _ in range(n):
            plasmapheresis = Plasmapheresis()
            plasmapheresis.patient = patient
            plasmapheresis.data_source = data_source
            plasmapheresis.from_date = random_date(patient.earliest_date_of_birth, date.today())

            if random.random() > 0.5:
                plasmapheresis.to_date = random_date(plasmapheresis.from_date, date.today())

            plasmapheresis.no_of_exchanges = random.choice(PLASMAPHERESIS_NO_OF_EXCHANGES.keys())
            plasmapheresis.response = random.choice(PLASMAPHERESIS_RESPONSES.keys())

            validate_and_add(plasmapheresis)

    return create_plasmapheresis


def create_renal_imaging_f():
    def create_renal_imaging(patient, data_source, n):
        for _ in range(n):
            renal_imaging = RenalImaging()
            renal_imaging.patient = patient
            renal_imaging.data_source = data_source
            renal_imaging.date = random_date(patient.earliest_date_of_birth, date.today())
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

            validate_and_add(renal_imaging)

    return create_renal_imaging


def create_patients(n):
    radar_data_source = get_radar_data_source()
    organisations = Organisation.query\
        .filter(Organisation.type == ORGANISATION_TYPE_UNIT)\
        .all()
    cohorts = Cohort.query.all()
    radar_organisation = get_radar_organisation()
    radar_cohort = get_radar_cohort()

    create_demographics = create_demographics_f()
    create_dialysis = create_dialysis_f()
    create_medications = create_medications_f()
    create_transplants = create_transplants_f()
    create_plasmapheresis = create_plasmapheresis_f()
    create_hospitalisations = create_hospitalisations_f()
    create_renal_imaging = create_renal_imaging_f()
    create_result_groups = create_result_groups_f()
    create_patient_aliases = create_patient_aliases_f()
    create_patient_numbers = create_patient_numbers_f()
    create_patient_addresses = create_patient_addresses_f()

    for i in range(n):
        print 'patient #%d' % (i + 1)

        patient = Patient()
        patient.is_active = True
        validate_and_add(patient)

        gender = generate_gender()

        create_demographics(patient, radar_data_source, gender)
        create_patient_aliases(patient, radar_data_source)
        create_patient_numbers(patient, radar_data_source)
        create_patient_addresses(patient, radar_data_source)

        radar_cohort_patient = CohortPatient()
        radar_cohort_patient.patient = patient
        radar_cohort_patient.cohort = radar_cohort
        radar_cohort_patient.recruited_date = random_datetime(datetime(2008, 1, 1, tzinfo=pytz.UTC), datetime.now(tz=pytz.UTC))
        radar_cohort_patient.recruited_by_organisation = radar_organisation
        radar_cohort_patient.is_active = True
        validate_and_add(radar_cohort_patient)

        for organisation in random.sample(organisations, random.randint(1, 3)):
            organisation_patient = OrganisationPatient()
            organisation_patient.organisation = organisation
            organisation_patient.patient = patient
            organisation_patient.is_active = True
            validate_and_add(organisation_patient)
            organisation_patient.created_date = random_datetime(patient.created_date, datetime.now(tz=pytz.UTC))

            if i < 5:
                for data_source in organisation.data_sources:
                    if data_source.type != DATA_SOURCE_TYPE_RADAR:
                        create_demographics(patient, data_source, gender)
                        create_patient_aliases(patient, data_source)
                        create_patient_numbers(patient, data_source)
                        create_patient_addresses(patient, data_source)

                    create_result_groups(patient, data_source, 10)
                    create_dialysis(patient, data_source, 5)
                    create_medications(patient, data_source, 5)
                    create_transplants(patient, data_source, 3)
                    create_hospitalisations(patient, data_source, 3)
                    create_plasmapheresis(patient, data_source, 3)
                    create_renal_imaging(patient, data_source, 3)

        cohort_patient = CohortPatient()

        if i == 0:
            cohort_patient.cohort = Cohort.query.filter(Cohort.code == 'INS').one()
        else:
            cohort_patient.cohort = random.choice(cohorts)

        cohort_patient.patient = patient
        cohort_patient.recruited_date = random_datetime(patient.created_date, datetime.now(tz=pytz.UTC))
        cohort_patient.recruited_by_organisation = radar_organisation
        cohort_patient.is_active = True
        validate_and_add(cohort_patient)


def create_data(patients_n=5, users_n=10):
    # Always generate the same "random" data
    random.seed(0)

    with db.session.no_autoflush:
        create_bot_user()
        create_admin_user()

        create_initial_data()

        create_southmead_user()
        create_srns_user()
        create_srns_demograhics_user()

        create_users(users_n)
        create_patients(patients_n)

        create_posts(10)
