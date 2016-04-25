import logging
import requests

from celery import Celery, chain
from flask import current_app

from radar.models.patients import Patient
from radar.models.groups import Group, GROUP_TYPE_HOSPITAL
from radar.models.logs import Log
from radar.database import db
from radar.groups import is_radar_group

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


def get_group(group_id):
    return Group.query.get(group_id)


def log_data_export(patient, group):
    log = Log()
    log.type = 'DATA_EXPORT'
    log.data = dict(
        patient_id=patient.id,
        group_id=group.id
    )
    db.session.add(log)


@celery.task
def export_sda(patient_id):
    patient = get_patient(patient_id)

    if patient is None:
        logger.error('Patient not found id={}'.format(patient_id))
        return

    groups = set(patient.groups)

    for group in groups:
        if not is_radar_group(group) and group.type != GROUP_TYPE_HOSPITAL:
            continue

        _export_sda(patient.id, group.id)


def _export_sda(patient_id, group_id):
    patient = get_patient(patient_id)

    if patient is None:
        logger.error('Patient not found id={}'.format(patient_id))
        return

    group = get_group(group_id)

    if group is None:
        logger.error('Group not found id={}'.format(group_id))
        return
    elif is_radar_group(group):
        facility = 'RADAR'
    else:
        facility = 'RADAR.{type}.{code}'.format(type=group.type, code=group.code)

    sda_container = {
        'sending_facility': facility
    }

    export_patient(sda_container, patient)

    export_medications(sda_container, patient, group)
    export_lab_orders(sda_container, patient, group)

    if group is None:
        export_program_memberships(sda_container, patient)

    # Convert date/datetime objects to ISO strings
    sda_container = transform_values(sda_container, to_iso)

    log_data_export(patient, group)

    db.session.commit()


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
