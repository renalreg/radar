import logging
import requests
import json
from decimal import Decimal

from celery import shared_task, chain
from flask import current_app

from radar.models.patients import Patient
from radar.models.groups import Group, GROUP_TYPE
from radar.models.logs import Log
from radar.database import db
from radar.groups import is_radar_group

from radar.ukrdc_exporter.medications import export_medications
from radar.ukrdc_exporter.patients import export_patient
from radar.ukrdc_exporter.results import export_lab_orders
from radar.ukrdc_exporter.groups import export_program_memberships
from radar.ukrdc_exporter.utils import transform_values, to_iso


logger = logging.getLogger(__name__)

QUEUE = 'ukrdc_exporter'


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


@shared_task(queue=QUEUE)
def export_sda(patient_id):
    patient = get_patient(patient_id)

    if patient is None:
        logger.error('Patient not found id={}'.format(patient_id))
        return

    groups = set(patient.groups)
    sda_containers = []

    for group in groups:
        if not is_radar_group(group) and group.type != GROUP_TYPE.HOSPITAL:
            continue

        sda_container = _export_sda(patient, group)
        sda_containers.append(sda_container)
        log_data_export(patient, group)

    db.session.commit()

    return sda_containers


def _export_sda(patient, group):
    if is_radar_group(group):
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

    return sda_container


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)

        return super(DecimalEncoder, self).default(o)


# TODO this can be done in parallel
@shared_task(bind=True, ignore_result=True, queue=QUEUE)
def send_to_ukrdc(self, sda_containers):
    config = current_app.config

    url = config['UKRDC_IMPORT_URL']
    timeout = config.get('UKRDC_IMPORT_TIMEOUT', 10)
    retry_countdown = config.get('UKRDC_IMPORT_COUNTDOWN', 60)

    for sda_container in sda_containers:
        data = json.dumps(sda_container, cls=DecimalEncoder)

        try:
            # Timeout if no bytes have been received on the underlying socket for TIMEOUT seconds
            r = requests.post(url, data=data, timeout=timeout)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.retry(exc=e, countdown=retry_countdown)


def export_to_ukrdc(patient_id):
    chain(export_sda.s(patient_id), send_to_ukrdc.s())()
