import json
import logging
import uuid

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from flask import Flask

from radar.models.patients import Patient
from radar.database import db

from aliases import import_aliases
from medications import import_medications
from addresses import import_addresses
from demographics import import_demographics
from patient_numbers import import_patient_numbers
from results import import_results

from utils import load_schema


logger = logging.getLogger(__name__)

NAMESPACE = uuid.UUID('91bce7f1-ea5f-4c98-8350-33d65d597a10')


class Fail(Exception):
    pass


def find_patient_id(sda_patient_numbers):
    """Find RaDaR number in patient numbers"""

    for sda_patient_number in sda_patient_numbers:
        if sda_patient_number['organization']['code'] == 'RADAR':
            return sda_patient_number['number']

    return None


def parse_patient_id(value):
    if isinstance(value, basestring):
        value = int(value)

    return value


def get_patient(patient_id):
    return Patient.query.get(patient_id)


def import_json(sda_container):
    schema = load_schema('schema.json')

    try:
        validate(sda_container, schema)
    except ValidationError:
        raise Fail('Invalid container')

    sda_patient = sda_container['patient']
    sda_patient_numbers = sda_patient['patient_numbers']

    patient_id = find_patient_id(sda_patient_numbers)

    if patient_id is None:
        raise Fail('No patient ID')

    try:
        patient_id = parse_patient_id(patient_id)
    except ValueError:
        raise Fail('Invalid patient ID')

    patient = get_patient(patient_id)

    if patient is None:
        raise Fail('Patient not found')

    sda_medications = sda_container.get('medications', list())
    sda_names = sda_container.get('aliases', list())
    sda_addresses = sda_container.get('addresses', list())
    sda_lab_orders = sda_container.get('lab_orders', list())

    import_demographics(patient, sda_patient)
    import_patient_numbers(patient, sda_patient_numbers)
    import_aliases(patient, sda_names)
    import_addresses(patient, sda_addresses)
    import_medications(patient, sda_medications)
    import_results(patient, sda_lab_orders)

    db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('RADAR_SETTINGS')

    # noinspection PyUnresolvedReferences
    from radar import models  # noqa

    db.init_app(app)

    return app


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    with open('test.json', 'rb') as f:
        sda_container = json.load(f)

    app = create_app()

    with app.app_context():
        import_json(sda_container)
