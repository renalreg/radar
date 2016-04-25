import logging
import requests

from celery import Celery, chain
from flask import current_app

from radar.models.patients import Patient

from radar_ukrdc_exporter.medications import export_medications
from radar_ukrdc_exporter.patients import export_patient
from radar_ukrdc_exporter.results import export_lab_orders
from radar_ukrdc_exporter.groups import export_program_memberships
from radar_ukrdc_exporter.utils import transform_values, to_iso


logger = logging.getLogger(__name__)


celery = Celery()
celery.conf.CELERY_DEFAULT_QUEUE = 'ukrdc_exporter'


def get_patient(patient_id):
    return Patient.query.get(patient_id)


@celery.task
def export_sda(patient_id):
    patient = get_patient(patient_id)

    if patient is None:
        logger.error('Patient not found id={}'.format(patient_id))
        return

    sda_container = {
        'sending_facility': 'RADAR'
    }

    export_patient(sda_container, patient)
    export_medications(sda_container, patient)
    export_lab_orders(sda_container, patient)
    export_program_memberships(sda_container, patient)

    # Convert date/datetime objects to ISO strings
    sda_container = transform_values(sda_container, to_iso)

    return sda_container


@celery.task(bind=True)
def send_to_ukrdc(self, sda_container):
    config = current_app.config['UKRDC_EXPORTER']

    url = config['URL']
    timeout = config.get('TIMEOUT', 10)
    retry_countdown = config.get('RETRY_COUNTDOWN', 60)

    try:
        # Timeout if no bytes have been received on the underlying socket for TIMEOUT seconds
        r = requests.post(url, json=sda_container, timeout=timeout)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        self.retry(exc=e, countdown=retry_countdown)


def export_to_ukrdc(patient_id):
    chain(export_sda.s(patient_id), send_to_ukrdc.s())()
