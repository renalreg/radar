import random
from datetime import timedelta, date, datetime

from sqlalchemy import desc
import pytz

from radar.database import db, no_autoflush
from radar.models.patient_demographics import PatientDemographics
from radar.models.patient_numbers import PatientNumber
from radar.models.patient_aliases import PatientAlias
from radar.models.patient_addresses import PatientAddress
from radar.models.patients import Patient, ETHNICITIES
from radar.models.source_types import SOURCE_TYPE_RADAR, SOURCE_TYPE_UKRDC
from radar.models.groups import (
    Group,
    GroupPatient,
    GROUP_TYPE,
    GROUP_CODE_NHS,
    GROUP_CODE_CHI,
    GROUP_CODE_UKRR,
    GROUP_CODE_NHSBT
)

from radar_fixtures.constants import GENDER_FEMALE
from radar_fixtures.dialysis import create_dialysis_f
from radar_fixtures.hospitalisations import create_hospitalisations_f
from radar_fixtures.medications import create_medications_f
from radar_fixtures.plasmapheresis import create_plasmapheresis_f
from radar_fixtures.renal_imaging import create_renal_imaging_f
from radar_fixtures.results import create_results_f
from radar_fixtures.transplants import create_transplants_f
from radar_fixtures.utils import (
    generate_first_name,
    generate_last_name,
    generate_first_name_alias,
    generate_date_of_birth,
    generate_date_of_death,
    generate_phone_number,
    generate_mobile_number,
    generate_email_address,
    generate_nhs_no,
    generate_chi_no,
    generate_ukrr_no,
    generate_nhsbt_no,
    generate_address_1,
    generate_address_2,
    generate_address_3,
    generate_postcode,
    random_date,
    random_datetime,
    generate_gender,
    add
)


def create_demographics_f():
    def create_demographics(patient, source_group, source_type, gender):
        old_d = PatientDemographics.query.filter(PatientDemographics.patient == patient).first()
        new_d = PatientDemographics()
        new_d.patient = patient
        new_d.source_group = source_group
        new_d.source_type = source_type

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

        add(new_d)

    return create_demographics


def create_patient_aliases_f():
    def create_patient_aliases(patient, source_group, source_type):
        d = PatientDemographics.query.filter(PatientDemographics.patient == patient).first()

        alias = PatientAlias()
        alias.patient = patient
        alias.source_group = source_group
        alias.source_type = source_type

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

        add(alias)

    return create_patient_aliases


def create_patient_numbers_f():
    number_groups = [
        (Group.query.filter(Group.code == GROUP_CODE_NHS, Group.type == GROUP_TYPE.OTHER).one(), generate_nhs_no),
        (Group.query.filter(Group.code == GROUP_CODE_CHI, Group.type == GROUP_TYPE.OTHER).one(), generate_chi_no),
        (Group.query.filter(Group.code == GROUP_CODE_UKRR, Group.type == GROUP_TYPE.OTHER).one(), generate_ukrr_no),
        (Group.query.filter(Group.code == GROUP_CODE_NHSBT, Group.type == GROUP_TYPE.OTHER).one(), generate_nhsbt_no),
    ]

    def create_patient_numbers(patient, source_group, source_type):
        for number_group, f in number_groups:
            old_n = PatientNumber.query.filter(PatientNumber.patient == patient, PatientNumber.number_group == number_group).first()
            new_n = PatientNumber()
            new_n.patient = patient
            new_n.source_group = source_group
            new_n.source_type = source_type
            new_n.number_group = number_group

            if old_n is None:
                new_n.number = f()
            else:
                new_n.number = old_n.number

            add(new_n)

    return create_patient_numbers


def create_patient_addresses_f():
    def create_patient_addresses(patient, source_group, source_type):
        old_a = PatientAddress.query\
            .filter(PatientAddress.patient == patient)\
            .order_by(desc(PatientAddress.from_date), desc(PatientAddress.to_date))\
            .first()

        new_a = PatientAddress()
        new_a.patient = patient
        new_a.source_group = source_group
        new_a.source_type = source_type

        if old_a is None:
            new_a.from_date = patient.earliest_date_of_birth
            new_a.address_1 = generate_address_1()
            new_a.address_2 = generate_address_2()
            new_a.address_3 = generate_address_3()
            new_a.postcode = generate_postcode()
        else:
            to_date = random_date(old_a.from_date, date.today())

            if random.random() > 0.5 and to_date != old_a.from_date:
                old_a.to_date = to_date
                new_a.from_date = to_date
                new_a.address_1 = generate_address_1()
                new_a.address_2 = generate_address_2()
                new_a.address_3 = generate_address_3()
                new_a.postcode = generate_postcode()
            else:
                new_a.from_date = old_a.from_date
                new_a.address_1 = old_a.address_1
                new_a.address_2 = old_a.address_2
                new_a.address_3 = old_a.address_3
                new_a.postcode = old_a.postcode

        add(new_a)

    return create_patient_addresses


@no_autoflush
def create_patients(n, data):
    radar_group = Group.get_radar()

    hospital_groups = Group.query.filter(Group.type == GROUP_TYPE.HOSPITAL).all()
    cohort_groups = Group.query.filter(Group.type == GROUP_TYPE.COHORT).all()

    source_types = [SOURCE_TYPE_RADAR, SOURCE_TYPE_UKRDC]

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
    create_results = create_results_f()

    for i in range(n):
        print 'patient #%d' % (i + 1)

        patient = Patient()
        add(patient)

        gender = generate_gender()

        create_demographics(patient, radar_group, SOURCE_TYPE_RADAR, gender)
        create_patient_aliases(patient, radar_group, SOURCE_TYPE_RADAR)
        create_patient_numbers(patient, radar_group, SOURCE_TYPE_RADAR)
        create_patient_addresses(patient, radar_group, SOURCE_TYPE_RADAR)

        recruited_date = random_datetime(datetime(2008, 1, 1, tzinfo=pytz.UTC), datetime.now(tz=pytz.UTC))

        radar_group_patient = GroupPatient()
        radar_group_patient.patient = patient
        radar_group_patient.group = radar_group
        radar_group_patient.from_date = recruited_date
        radar_group_patient.created_group = radar_group
        add(radar_group_patient)

        for hospital_group in random.sample(hospital_groups, random.randint(1, min(3, len(hospital_groups)))):
            hospital_group_patient = GroupPatient()
            hospital_group_patient.group = hospital_group
            hospital_group_patient.patient = patient
            hospital_group_patient.from_date = random_datetime(recruited_date, datetime.now(tz=pytz.UTC))
            hospital_group_patient.created_group = radar_group
            add(hospital_group_patient)

            if data:
                for source_type in source_types:
                    if source_type != SOURCE_TYPE_RADAR:
                        create_demographics(patient, hospital_group, source_type, gender)
                        create_patient_aliases(patient, hospital_group, source_type)
                        create_patient_numbers(patient, hospital_group, source_type)
                        create_patient_addresses(patient, hospital_group, source_type)

                    create_dialysis(patient, hospital_group, source_type, 5)
                    create_medications(patient, hospital_group, source_type, 5)
                    create_transplants(patient, hospital_group, source_type, 3)
                    create_hospitalisations(patient, hospital_group, source_type, 3)
                    create_plasmapheresis(patient, hospital_group, source_type, 3)
                    create_renal_imaging(patient, hospital_group, source_type, 3)
                    create_results(patient, hospital_group, source_type, 10, 25)

        cohort_group_patient = GroupPatient()
        cohort_group_patient.group = random.choice(cohort_groups)
        cohort_group_patient.patient = patient
        cohort_group_patient.from_date = random_datetime(recruited_date, datetime.now(tz=pytz.UTC))
        cohort_group_patient.created_group = radar_group
        add(cohort_group_patient)
