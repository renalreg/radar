from datetime import date, datetime
from decimal import Decimal
import json
import logging

from celery import shared_task
import requests

from radar.config import config
from radar.database import db
from radar.models.groups import Group, GROUP_TYPE
from radar.models.logs import Log
from radar.models.patients import Patient
from radar.ukrdc_exporter.groups import export_program_memberships
from radar.ukrdc_exporter.medications import export_medications
from radar.ukrdc_exporter.patients import export_patient
from radar.ukrdc_exporter.results import export_lab_orders
from radar.ukrdc_exporter.utils import to_iso, transform_values


logger = logging.getLogger(__name__)

QUEUE = 'ukrdc_exporter'


def get_patient(patient_id):
    return Patient.query.get(patient_id)


def get_group(group_id):
    return Group.query.get(group_id)


def log_data_export(patient, system_group, group=None):
    data = {
        'patient_id': patient.id,
        'system_group_id': system_group.id,
    }

    if group is not None:
        data['group_id'] = group.id

    log = Log()
    log.type = 'UKRDC_EXPORTER'
    log.data = data
    db.session.add(log)


@shared_task(ignore_result=True, queue=QUEUE)
def export_sda(patient_id):
    patient = get_patient(patient_id)

    if patient is None:
        logger.error('Patient not found id={}'.format(patient_id))
        return

    if patient.test:
        logger.info('Skipping test patient id={}'.format(patient_id))
        return

    groups = set(patient.groups)
    jobs = []

    for group1 in groups:
        if group1.type == GROUP_TYPE.HOSPITAL:
            # Export a hospital for each system
            for group2 in groups:
                if group2.type == GROUP_TYPE.SYSTEM:
                    jobs.append((group2, group1))
        elif group1.type == GROUP_TYPE.SYSTEM:
            jobs.append((group1, None))

    for system_group, group in jobs:
        sda_container = _export_sda(patient, system_group, group)
        send_to_ukrdc.delay(sda_container)
        log_data_export(patient, system_group, group)

    db.session.commit()


def _export_sda(patient, system_group, group=None):
    if group is None:
        facility = system_group.code
        group = system_group
    else:
        facility = '{0}.{1}.{2}'.format(system_group.code, group.type, group.code)

    sda_container = {
        'sending_facility': facility
    }

    export_patient(sda_container, patient, system_group)
    export_medications(sda_container, patient, group)
    export_lab_orders(sda_container, patient, group)

    if group.type == GROUP_TYPE.SYSTEM:
        export_program_memberships(sda_container, patient, system_group)

    # Convert date/datetime objects to ISO strings
    sda_container = transform_values(sda_container, to_iso)

    return sda_container


class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        elif isinstance(o, datetime):
            # HS doesn't handle microseconds
            o = o.replace(microsecond=0)
            return o.isoformat()
        elif isinstance(o, date):
            return o.isoformat()

        return super(Encoder, self).default(o)


@shared_task(bind=True, ignore_result=True, queue=QUEUE)
def send_to_ukrdc(self, sda_container):
    url = config['UKRDC_EXPORTER_URL']
    timeout = config.get('UKRDC_EXPORTER_TIMEOUT', 60)
    retry_countdown = config.get('UKRDC_EXPORTER_COUNTDOWN', 60)

    data = json.dumps(sda_container, cls=Encoder)

    try:
        # Timeout if no bytes have been received on the underlying socket for TIMEOUT seconds
        r = requests.post(url, data=data, timeout=timeout, headers={'Content-Type': 'application/json'})
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        self.retry(exc=e, countdown=retry_countdown)


def export_to_ukrdc(patient_id):
    export_sda.delay(patient_id)
