import string
import random
import uuid
from datetime import datetime, timedelta

from radar.models.groups import Group
from radar.models.patients import Patient

from radar_ukrdc.tasks import import_sda, create_app
from radar_ukrdc.utils import utc


def random_string(alphabet, n):
    return ''.join(random.choice(alphabet) for _ in xrange(n))


def random_datetime():
    start_dt = datetime(1900, 1, 1)
    end_dt = datetime.now()
    seconds = random.randint(0, (end_dt - start_dt).total_seconds())
    dt = start_dt + timedelta(seconds=seconds)
    return dt.isoformat()


def generate_patient_numbers(patient, n):
    groups = Group.query.filter(Group.code != 'RADAR').all()
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

    for _ in xrange(n):
        aliases.append({
            'given_name': random_string(string.ascii_letters, 10),
            'family_name': random_string(string.ascii_letters, 10)
        })

    return aliases


def generate_addresses(n):
    addresses = []

    for _ in xrange(n):
        street = random_string(string.ascii_letters, 10)
        city = random_string(string.ascii_letters, 10)
        state = random_string(string.ascii_letters, 10)
        country = random_string(string.ascii_letters, 10)
        zip = random_string(string.ascii_letters, 10)

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
                'code': zip,
                'description': zip
            }
        })

    return addresses


def generate_medications(n):
    group = random.choice(Group.query.all())
    medications = []

    for i in xrange(n):
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
    for _ in xrange(n):
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


if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        stress(1000)
