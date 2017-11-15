#!/usr/bin/env python

import argparse
from datetime import datetime, timedelta
import random
import string
import uuid

from radar.models.groups import Group, GROUP_TYPE
from radar.models.patients import Patient
from radar.ukrdc_importer.app import RadarUKRDCImporter
from radar.ukrdc_importer.tasks import import_sda
from radar.ukrdc_importer.utils import utc


def random_string(alphabet, n):
    return ''.join(random.choice(alphabet) for _ in range(n))


def random_datetime():
    start_dt = datetime(1900, 1, 1)
    end_dt = datetime.now()
    seconds = random.randint(0, int((end_dt - start_dt).total_seconds()))
    dt = start_dt + timedelta(seconds=seconds)
    return dt.isoformat()


def generate_patient_numbers(patient, n):
    groups = Group.query.filter(Group.type != GROUP_TYPE.SYSTEM).all()
    groups = random.sample(groups, min(len(groups), n))

    patient_numbers = [{
        'number': str(patient.id),
        'number_type': 'MRN',
        'organization': {
            'code': 'RADAR',
            'description': 'RADAR'
        }
    }]

    for group in groups:
        patient_numbers.append({
            'number': str(uuid.uuid4()),
            'number_type': 'MRN',
            'organization': {
                'code': group.code,
                'description': group.name
            }
        })

    return patient_numbers


def generate_aliases(n):
    aliases = []

    for _ in range(n):
        aliases.append({
            'given_name': random_string(string.ascii_letters, 10),
            'family_name': random_string(string.ascii_letters, 10)
        })

    return aliases


def generate_addresses(n):
    addresses = []

    for _ in range(n):
        street = random_string(string.ascii_letters, 10)
        city = random_string(string.ascii_letters, 10)
        state = random_string(string.ascii_letters, 10)
        country = random_string(string.ascii_letters, 10)
        post_code = random_string(string.ascii_letters, 10)

        addresses.append({
            'street': street,
            'city': {
                'code': city,
                'description': city
            },
            'state': {
                'code': state,
                'description': state
            },
            'country': {
                'code': country,
                'description': country
            },
            'zip': {
                'code': post_code,
                'description': post_code
            }
        })

    return addresses


def generate_medications(n):
    group = random.choice(Group.query.all())
    medications = []

    for i in range(n):
        name = random_string(string.ascii_letters, 10)
        dose = random_string(string.ascii_letters, 10)
        from_time = random_datetime()
        to_time = random_datetime()

        medications.append({
            'external_id': str(i),
            'from_time': from_time,
            'to_time': to_time,
            'drug_product': {
                'product_name': name
            },
            'dose_u_o_m': {
                'code': dose,
                'description': dose
            },
            'entering_organization': {
                'code': group.code,
                'description': group.name
            }
        })

    return medications


def stress(n):
    for _ in range(n):
        _stress()


def _stress():
    patients = Patient.query.all()
    patient = random.choice(patients)

    sda_container = {
        'patient': {
            'name': {
                'given_name': random_string(string.ascii_letters, 10),
                'family_name': random_string(string.ascii_letters, 10)
            },
            'birth_time': random_datetime(),
            'death_time': random_datetime(),
            'gender': {
                'code': '1',
                'description': 'Male'
            },
            'ethnic_group': {
                'code': 'A',
                'description': 'British'
            },
            'contact_info': {
                'home_phone_number': random_string(string.digits, 10),
                'mobile_phone_number': random_string(string.digits, 10),
                'work_phone_number': random_string(string.digits, 10),
                'email_address': 'foo@example.org'
            },
            'patient_numbers': generate_patient_numbers(patient, 10),
            'aliases': generate_aliases(10),
            'addresses': generate_addresses(10)
        },
        'medications': generate_medications(100)
    }

    sequence_number = utc()
    import_sda.delay(sda_container, sequence_number)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int)
    args = parser.parse_args()

    app = RadarUKRDCImporter()

    with app.app_context():
        stress(args.n)


if __name__ == '__main__':
    main()
