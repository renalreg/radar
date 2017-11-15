from datetime import date, datetime, timedelta
import random

import pytz
from sqlalchemy import desc

from radar.database import no_autoflush
from radar.fixtures.constants import GENDER_FEMALE
from radar.fixtures.dialysis import create_dialysis_f
from radar.fixtures.hospitalisations import create_hospitalisations_f
from radar.fixtures.medications import create_medications_f
from radar.fixtures.plasmapheresis import create_plasmapheresis_f
from radar.fixtures.renal_imaging import create_renal_imaging_f
from radar.fixtures.results import create_results_f
from radar.fixtures.transplants import create_transplants_f
from radar.fixtures.utils import (
    add,
    generate_address1,
    generate_address2,
    generate_address3,
    generate_chi_no,
    generate_date_of_birth,
    generate_date_of_death,
    generate_email_address,
    generate_first_name,
    generate_first_name_alias,
    generate_gender,
    generate_last_name,
    generate_mobile_number,
    generate_nhs_no,
    generate_nhsbt_no,
    generate_phone_number,
    generate_postcode,
    generate_ukrr_no,
    random_date,
    random_datetime,
)
from radar.models.demographics import Ethnicity
from radar.models.groups import (
    Group,
    GROUP_CODE_CHI,
    GROUP_CODE_NHS,
    GROUP_CODE_NHSBT,
    GROUP_CODE_UKRR,
    GROUP_TYPE,
    GroupPatient,
)
from radar.models.patient_addresses import PatientAddress
from radar.models.patient_aliases import PatientAlias
from radar.models.patient_codes import ETHNICITIES
from radar.models.patient_demographics import PatientDemographics
from radar.models.patient_numbers import PatientNumber
from radar.models.patients import Patient
from radar.models.source_types import SOURCE_TYPE_MANUAL, SOURCE_TYPE_UKRDC


def create_ethnicities():
    for code, label in ETHNICITIES.items():
        ethnicity = Ethnicity(code=code, label=label)
        add(ethnicity)


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
            new_d.ethnicity = random.choice(Ethnicity.query.all())

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
            old_n = PatientNumber.query.filter(
                PatientNumber.patient == patient,
                PatientNumber.number_group == number_group).first()
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
            new_a.address1 = generate_address1()
            new_a.address2 = generate_address2()
            new_a.address3 = generate_address3()
            new_a.postcode = generate_postcode()
            new_a.country = 'GB'
        else:
            to_date = random_date(old_a.from_date, date.today())

            if random.random() > 0.5 and to_date != old_a.from_date:
                old_a.to_date = to_date
                new_a.from_date = to_date
                new_a.address1 = generate_address1()
                new_a.address2 = generate_address2()
                new_a.address3 = generate_address3()
                new_a.postcode = generate_postcode()
                new_a.country = 'GB'
            else:
                new_a.from_date = old_a.from_date
                new_a.address1 = old_a.address1
                new_a.address2 = old_a.address2
                new_a.address3 = old_a.address3
                new_a.postcode = old_a.postcode
                new_a.country = old_a.country

        add(new_a)

    return create_patient_addresses


@no_autoflush
def create_patients(n, data=True):
    hospital_groups = Group.query.filter(Group.type == GROUP_TYPE.HOSPITAL).all()
    cohort_groups = Group.query.filter(Group.type == GROUP_TYPE.COHORT).all()

    source_types = [SOURCE_TYPE_MANUAL, SOURCE_TYPE_UKRDC]

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
        print('patient #%d' % (i + 1))

        patient = Patient()
        add(patient)

        recruited_date = random_datetime(datetime(2008, 1, 1, tzinfo=pytz.UTC), datetime.now(tz=pytz.UTC))

        cohort_group = random.choice(cohort_groups)
        system_group = cohort_group.parent_group

        cohort_group_patient = GroupPatient()
        cohort_group_patient.group = cohort_group
        cohort_group_patient.patient = patient
        cohort_group_patient.from_date = random_datetime(recruited_date, datetime.now(tz=pytz.UTC))
        cohort_group_patient.created_group = system_group
        add(cohort_group_patient)

        system_group_patient = GroupPatient()
        system_group_patient.patient = patient
        system_group_patient.group = system_group
        system_group_patient.from_date = recruited_date
        system_group_patient.created_group = system_group
        add(system_group_patient)

        gender = generate_gender()

        create_demographics(patient, system_group, SOURCE_TYPE_MANUAL, gender)
        create_patient_aliases(patient, system_group, SOURCE_TYPE_MANUAL)
        create_patient_numbers(patient, system_group, SOURCE_TYPE_MANUAL)
        create_patient_addresses(patient, system_group, SOURCE_TYPE_MANUAL)

        for hospital_group in random.sample(hospital_groups, random.randint(1, min(3, len(hospital_groups)))):
            hospital_group_patient = GroupPatient()
            hospital_group_patient.group = hospital_group
            hospital_group_patient.patient = patient
            hospital_group_patient.from_date = random_datetime(recruited_date, datetime.now(tz=pytz.UTC))
            hospital_group_patient.created_group = system_group
            add(hospital_group_patient)

            if data:
                for source_type in source_types:
                    if source_type != SOURCE_TYPE_MANUAL:
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
