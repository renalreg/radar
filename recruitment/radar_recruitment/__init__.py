import logging
import calendar
from datetime import datetime

import requests
from celery import Celery
from flask import current_app
from jsonschema import ValidationError

from radar.models.patients import Patient, GENDERS
from radar.models.patient_numbers import PatientNumber


logger = logging.getLogger(__name__)


celery = Celery()
celery.conf.CELERY_DEFAULT_QUEUE = 'ukrdc_importer'


class ApiError(Exception):
    """An exception occurred while calling the API."""


class DemographicsMismatch(Exception):
    """Demographic details on record don't match the supplied details."""


class SearchPatient(object):
    def __init__(self, first_name, last_name, date_of_birth, gender, number, number_group):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = gender
        self.gender = gender
        self.number = number
        self.number_group = number_group

    def search_ukrdc(self):
        url = current_app.config['UKRDC_SEARCH_URL']
        timeout = current_app.config.get('UKRDC_SEARCH_TIMEOUT', 60)

        data = {
            'patient': {
                'name': {
                    'given_name': self.first_name,
                    'family_name': self.last_name
                },
                'gender': {
                    'code': str(self.gender),
                    'description': GENDERS[self.gender]
                },
                'birth_time': self.date_of_birth.isoformat(),
                'patient_numbers': [
                    {
                        'number': self.number,
                        'number_type': 'NI',
                        'organization': {
                            'code': self.number_group.code,
                            'description': self.number_group.name
                        }
                    }
                ]
            }
        }

        try:
            r = requests.post(url, json=data, timeout=timeout)

            if r.status_code == 404:
                return None
            else:
                r.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ApiError(e)

        try:
            data = r.json()
        except ValueError as e:
            raise ApiError(e)

        try:
            sda_container = SDAContainer(data)
        except ValueError as e:
            raise ApiError(e)

        return sda_container

    def _check_demographics(self, patient):
        names = patient.first_names + patient.last_names
        dates_of_birth = patient.dates_of_birth
        genders = patient.genders

        # TODO
        return True

    def _search_radar(self):
        q = Patient.query
        q = q.join(Patient.patient_numbers)
        q = q.filter(PatientNumber.number == self.number)
        q = q.filter(PatientNumber.number_group == self.number_group)
        patient = q.first()
        return patient

    def search_radar(self):
        patient = self.search_radar()

        if patient is not None and not self._check_demographics(patient):
            raise DemographicsMismatch

        return patient


class RecruitmentPatient(object):
    def __init__(self, search_patient, cohort_group, hospital_group, ethnicity=None):
        self.search_patient = search_patient
        self.cohort_group = cohort_group
        self.hospital_group = hospital_group
        self.ethnicity = None

    def search_radar(self):
        return self.search_patient.search_ukrdc()

    def search_ukrdc(self):
        return self.search_patient.search_ukrdc()

    def save(self):
        # TODO logging

        patient = self.search_radar()
        sda_container = None

        if patient is None:
            try:
                sda_container = self.search_ukrdc()
            except ApiError:
                # TODO log error
                pass

        if patient is None:
            # TODO create patient
            pass
        else:
            # TODO update patient
            pass

        # TODO commit

        if sda_container is not None:
            sda_container.save(patient=patient)

        return patient


class SDAContainer(object):
    def __init__(self, data):
        self.data = data
        self._validate()

    def _validate(self):
        # TODO
        pass

    def _get_sequence_number(self):
        return calendar.timegm(datetime.utcnow().utctimetuple())

    def save(self, patient=None):
        sequence_number = self._get_sequence_number()

        kwargs = {}

        if patient is not None:
            kwargs['patient_id'] = patient.id

        # TODO add patient_id kwarg
        celery.send_task('radar_ukrdc_importer.tasks.import_sda', args=[self.data, sequence_number], kwargs=kwargs)


def setup(app):
    setup_celery(app)


def setup_celery(app):
    config = app.config.get('UKRDC_IMPORTER', dict())

    broker_url = config.get('CELERY_BROKER_URL')

    if broker_url is not None:
        celery.conf.BROKER_URL = broker_url

    celery.conf.update(config)
