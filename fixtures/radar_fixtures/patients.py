import random
from datetime import timedelta, date, datetime

from sqlalchemy import desc
import pytz

from radar.models.patients import ETHNICITIES
from radar.models.patient_demographics import PatientDemographics
from radar.models.patient_numbers import PatientNumber
from radar.models.patient_aliases import PatientAlias
from radar.models.patient_addresses import PatientAddress
from radar.models.cohorts import Cohort, CohortPatient
from radar.models.organisations import Organisation, OrganisationPatient, ORGANISATION_TYPE_UNIT
from radar.models.patients import Patient
from radar.models.data_sources import DATA_SOURCE_TYPE_RADAR
from radar_fixtures.utils import generate_first_name, generate_last_name, generate_first_name_alias, \
    generate_date_of_birth, generate_date_of_death, generate_phone_number, generate_mobile_number, \
    generate_email_address, generate_nhs_no, generate_chi_no, generate_ukrr_no, generate_nhsbt_no, \
    generate_address1, generate_address2, generate_address3, generate_postcode, random_date, \
    random_datetime, generate_gender
from radar_fixtures.constants import GENDER_FEMALE
from radar_fixtures.validation import validate_and_add
from radar.organisations import get_nhs_organisation, get_chi_organisation, get_ukrr_organisation, get_nhsbt_organisation, get_radar_organisation
from radar.cohorts import get_radar_cohort
from radar.data_sources import get_radar_data_source
from radar_fixtures.dialysis import create_dialysis_f
from radar_fixtures.medications import create_medications_f
from radar_fixtures.transplants import create_transplants_f
from radar_fixtures.plasmapheresis import create_plasmapheresis_f
from radar_fixtures.hospitalisations import create_hospitalisations_f
from radar_fixtures.renal_imaging import create_renal_imaging_f


def create_demographics_f():
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
            new_d.ethnicity = random.choice(ETHNICITIES.keys())

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

            new_d.ethnicity = old_d.ethnicity
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
            new_a.address1 = generate_address1()
            new_a.address2 = generate_address2()
            new_a.address3 = generate_address3()
            new_a.postcode = generate_postcode()
        else:
            to_date = random_date(old_a.from_date, date.today())

            if random.random() > 0.5 and to_date != old_a.from_date:
                old_a.to_date = to_date
                new_a.from_date = to_date
                new_a.address1 = generate_address1()
                new_a.address2 = generate_address2()
                new_a.address3 = generate_address3()
                new_a.postcode = generate_postcode()
            else:
                new_a.from_date = old_a.from_date
                new_a.address1 = old_a.address1
                new_a.address2 = old_a.address2
                new_a.address3 = old_a.address3
                new_a.postcode = old_a.postcode

        validate_and_add(new_a)

    return create_patient_addresses


def create_patients(n):
    radar_data_source = get_radar_data_source()
    organisations = Organisation.query\
        .filter(Organisation.type == ORGANISATION_TYPE_UNIT)\
        .all()
    cohorts = Cohort.query.filter(Cohort.code != 'RADAR').all()
    radar_organisation = get_radar_organisation()
    radar_cohort = get_radar_cohort()

    create_demographics = create_demographics_f()
    create_dialysis = create_dialysis_f()
    create_medications = create_medications_f()
    create_transplants = create_transplants_f()
    create_plasmapheresis = create_plasmapheresis_f()
    create_hospitalisations = create_hospitalisations_f()
    create_renal_imaging = create_renal_imaging_f()
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

        recruited_date = random_datetime(datetime(2008, 1, 1, tzinfo=pytz.UTC), datetime.now(tz=pytz.UTC))

        radar_cohort_patient = CohortPatient()
        radar_cohort_patient.patient = patient
        radar_cohort_patient.cohort = radar_cohort
        radar_cohort_patient.recruited_date = recruited_date
        radar_cohort_patient.recruited_organisation = radar_organisation
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
        cohort_patient.recruited_date = random_datetime(recruited_date, datetime.now(tz=pytz.UTC))
        cohort_patient.recruited_organisation = radar_organisation
        cohort_patient.is_active = True
        validate_and_add(cohort_patient)
