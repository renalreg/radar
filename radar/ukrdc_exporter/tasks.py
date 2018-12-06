from datetime import date, datetime
from decimal import Decimal
import json
import logging

from celery import shared_task
import requests

from radar.config import config
from radar.database import db
from radar.models.groups import Group
from radar.models.logs import Log
from radar.models.patients import Patient
from radar.ukrdc_exporter.groups import export_program_memberships
# from radar.ukrdc_exporter.medications import export_medications
from radar.ukrdc_exporter.patients import export_patient
# from radar.ukrdc_exporter.results import export_lab_orders
from radar.ukrdc_exporter.utils import to_iso, transform_values


logger = logging.getLogger(__name__)

QUEUE = 'ukrdc_exporter'


def get_patient(patient_id):
    return Patient.query.get(patient_id)


def get_group(group_id):
    return Group.query.get(group_id)


def log_data_export(patient):
    data = {
        'patient_id': patient.id
    }

    log = Log()
    log.type = 'UKRDC_EXPORTER'
    log.data = data
    db.session.add(log)


@shared_task(ignore_result=True, queue=QUEUE)
def export_rda(patient_id):
    patient = get_patient(patient_id)

    if patient is None:
        logger.error('Patient not found id={}'.format(patient_id))
        return

    if patient.test:
        logger.info('Skipping test patient id={}'.format(patient_id))
        return

    groups = set(patient.groups)

    rda_container = _export_rda(patient, groups)
    send_to_ukrdc.delay(rda_container)

    log_data_export(patient)

    db.session.commit()


def _export_rda(patient, groups):

    rda_container = {
        'sending_facility': patient.recruited_group().code
    }

    export_patient(rda_container, patient, groups)
    export_program_memberships(rda_container, patient, groups)
    rda_container = transform_values(rda_container, to_iso)

    return rda_container


class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, date):
            return o.isoformat()

        return super(Encoder, self).default(o)


@shared_task(bind=True, ignore_result=True, queue=QUEUE)
def send_to_ukrdc(self, rda_container):
    url = config['UKRDC_EXPORTER_URL']
    timeout = config.get('UKRDC_EXPORTER_TIMEOUT', 60)
    retry_countdown = config.get('UKRDC_EXPORTER_COUNTDOWN', 60)

    data = json.dumps(rda_container, cls=Encoder)

    try:
        # Timeout if no bytes have been received on the underlying socket for TIMEOUT seconds
        r = requests.post(url, data=data, timeout=timeout, headers={'Content-Type': 'application/json'})
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        self.retry(exc=e, countdown=retry_countdown)


def export_to_ukrdc(patient_id):
    export_rda.delay(patient_id)
