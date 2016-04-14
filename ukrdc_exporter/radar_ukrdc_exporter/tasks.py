import logging
import requests
from flask import Flask
from celery import Celery, chain

from radar.database import db
from radar.models.patients import Patient

from radar_ukrdc_exporter.medications import export_medications
from radar_ukrdc_exporter.patients import export_patient
from radar_ukrdc_exporter.results import export_lab_orders
from radar_ukrdc_exporter.groups import export_program_memberships


logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('RADAR_SETTINGS')

    # noinspection PyUnresolvedReferences
    from radar import models  # noqa

    db.init_app(app)

    return app


def create_celery():
    app = create_app()

    celery = Celery(app.import_name)
    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


celery = create_celery()


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

    # TODO datetime to iso-8601

    return sda_container


@celery.task(bind=True)
def send_to_ukrdc(self, sda_container):
    # TODO url config
    # TODO timeout config
    # TODO retry config

    # TODO
    url = ''

    try:
        # Timeout if no bytes have been received on the underlying socket for 10 seconds
        r = requests.post(url, json=sda_container, timeout=10)
        r.raise_for_status()
    except requests.exceptions.RequestError:
        self.retry(countdown=60)


def export_to_ukrdc(patient_id):
    chain(export_sda.s(patient_id), send_to_ukrdc.s())


if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        print export_sda(1)
