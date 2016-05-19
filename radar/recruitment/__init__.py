import logging
import calendar
import re
import itertools
from datetime import datetime

import requests
import pytz

from radar.auth.sessions import current_user
from radar.config import config
from radar.database import db
from radar.models.groups import Group, GroupPatient
from radar.models.patient_demographics import PatientDemographics
from radar.models.patient_numbers import PatientNumber
from radar.models.patients import Patient, GENDERS
from radar.models.source_types import SOURCE_TYPE_RADAR
from radar.ukrdc_importer.tasks import import_sda


logger = logging.getLogger(__name__)


class ApiError(Exception):
    """An exception occurred while calling the API."""


class DemographicsMismatch(Exception):
    """Demographic details on record don't match the supplied details."""

    def __init__(self, patient):
        super(DemographicsMismatch, self).__init__(patient)
        self.patient = patient


class SearchPatient(object):
    def __init__(self, first_name, last_name, date_of_birth, gender, number_group, number):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.number_group = number_group
        self.number = number

    def search_ukrdc(self):
        enabled = config['UKRDC_SEARCH_ENABLED']

        if not enabled:
            logger.info('UKRDC search is disabled')
            return None

        logger.info('Searching UKRDC number={}'.format(self.number))

        url = config['UKRDC_SEARCH_URL']
        timeout = config.get('UKRDC_SEARCH_TIMEOUT', 60)
        username = config.get('UKRDC_SEARCH_USERNAME', 'RADAR')
        password = config.get('UKRDC_SEARCH_PASSWORD', 'password')

        data = {
            'patient': {
                'name': {
                    'given_name': self.first_name,
                    'family_name': self.last_name
                },
                'birth_time': self.date_of_birth.isoformat(),
                'gender': {
                    'code': str(self.gender),
                    'description': GENDERS[self.gender]
                },
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
            r = requests.post(url, json=data, timeout=timeout, auth=(username, password))

            if r.status_code == 404:
                logger.info('UKRDC patient not found')
                return None
            else:
                r.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.exception('API error')
            raise ApiError(e)

        try:
            data = r.json()
        except ValueError as e:
            logger.exception('Error decoding JSON')
            raise ApiError(e)

        logger.info('UKRDC patient found')

        return SDAContainer(data)

    def _check_name(self, patient, name, n):
        a = set(x[:n] for x in _split_names(patient.first_names + patient.last_names))
        b = set(x[:n] for x in _split_name(name))
        return len(a) == 0 or a.intersection(b)

    def _check_first_name(self, patient):
        return self._check_name(patient, self.first_name, 1)

    def _check_last_name(self, patient):
        return self._check_name(patient, self.last_name, 3)

    def _check_date_of_birth(self, patient):
        dates_of_birth = patient.dates_of_birth

        if len(dates_of_birth) == 0:
            return True

        for date_of_birth in dates_of_birth:
            year_match = self.date_of_birth.year == date_of_birth.year
            month_match = self.date_of_birth.month == date_of_birth.month
            day_match = self.date_of_birth.day == date_of_birth.day

            # Month and day swapped
            if (
                self.date_of_birth.month == date_of_birth.day and
                self.date_of_birth.day == date_of_birth.month
            ):
                month_match = True
                day_match = True

            # Two parts match
            if sum([year_match, month_match, day_match]) >= 2:
                return True

        return False

    def _check_gender(self, patient):
        genders = patient.genders
        return len(genders) == 0 or self.gender in genders

    def _check_demographics(self, patient):
        return (
            self._check_first_name(patient) and
            self._check_last_name(patient) and
            self._check_date_of_birth(patient) and
            self._check_gender(patient)
        )

    def _search_radar(self):
        logger.info('Searching RaDaR number={}'.format(self.number))

        q = Patient.query
        q = q.join(Patient.patient_numbers)
        q = q.filter(PatientNumber.number == self.number)
        q = q.filter(PatientNumber.number_group == self.number_group)
        patient = q.first()

        if patient is not None:
            logger.info('Found RaDaR patient id={}'.format(patient.id))
        else:
            logger.info('RaDaR patient not found')

        return patient

    def search_radar(self):
        patient = self._search_radar()

        if patient is not None and not self._check_demographics(patient):
            logger.error(
                'Demographics mismatch '
                'id={id} '
                'first_name={first_name} '
                'last_name={last_name} '
                'date_of_birth={date_of_birth} '
                'gender={gender}'.format(
                    id=patient.id,
                    first_name=self.first_name,
                    last_name=self.last_name,
                    date_of_birth=self.date_of_birth.strftime('%d/%m/%Y'),
                    gender=self.gender,
                )
            )

            raise DemographicsMismatch(patient)

        return patient


class RecruitmentPatient(object):
    def __init__(self, search_patient, cohort_group, hospital_group, ethnicity=None):
        self.search_patient = search_patient
        self.cohort_group = cohort_group
        self.hospital_group = hospital_group
        self.ethnicity = None

    @property
    def first_name(self):
        return self.search_patient.first_name

    @property
    def last_name(self):
        return self.search_patient.last_name

    @property
    def date_of_birth(self):
        return self.search_patient.date_of_birth

    @property
    def gender(self):
        return self.search_patient.gender

    @property
    def number_group(self):
        return self.search_patient.number_group

    @property
    def number(self):
        return self.search_patient.number

    def search_radar(self):
        return self.search_patient.search_radar()

    def search_ukrdc(self):
        return self.search_patient.search_ukrdc()

    def _create_patient(self):
        logger.info('Creating patient number={}'.format(self.number))

        radar_group = Group.get_radar()

        patient = Patient()
        patient.created_user = current_user
        patient.modified_user = current_user
        db.session.add(patient)

        radar_group_patient = GroupPatient()
        radar_group_patient.patient = patient
        radar_group_patient.group = radar_group
        radar_group_patient.created_group = self.hospital_group
        radar_group_patient.from_date = datetime.now(pytz.UTC)
        radar_group_patient.created_user = current_user
        radar_group_patient.modified_user = current_user
        db.session.add(radar_group_patient)

        patient_demographics = PatientDemographics()
        patient_demographics.patient = patient
        patient_demographics.source_group = radar_group
        patient_demographics.source_type = SOURCE_TYPE_RADAR
        patient_demographics.first_name = self.first_name
        patient_demographics.last_name = self.last_name
        patient_demographics.date_of_birth = self.date_of_birth
        patient_demographics.gender = self.gender
        patient_demographics.ethnicity = self.ethnicity
        patient_demographics.created_user = current_user
        patient_demographics.modified_user = current_user
        db.session.add(patient_demographics)

        patient_number = PatientNumber()
        patient_number.patient = patient
        patient_number.source_group = radar_group
        patient_number.source_type = SOURCE_TYPE_RADAR
        patient_number.number_group = self.number_group
        patient_number.number = self.number
        patient_number.created_user = current_user
        patient_number.modified_user = current_user
        db.session.add(patient_number)

        return patient

    def _add_to_group(self, patient, group):
        # Add the patient to the cohort group
        if not patient.in_group(group, current=True):
            logger.info('Adding patient number={} to group id={}'.format(self.number, group.id))

            group_patient = GroupPatient()
            group_patient.patient = patient
            group_patient.group = group
            group_patient.created_group = self.hospital_group
            group_patient.from_date = datetime.now(pytz.UTC)
            group_patient.created_user = current_user
            group_patient.modified_user = current_user
            db.session.add(group_patient)

    def _update_patient(self, patient):
        self._add_to_group(patient, self.hospital_group)
        self._add_to_group(patient, self.cohort_group)

    def save(self):
        patient = self.search_radar()
        sda_container = None

        # New patient
        if patient is None:
            try:
                sda_container = self.search_ukrdc()
            except ApiError:
                pass

            patient = self._create_patient()

        self._update_patient(patient)

        db.session.commit()

        if sda_container is not None:
            sda_container.save(patient)

        return patient


class SDAContainer(object):
    def __init__(self, data):
        self.data = data

    def _get_sequence_number(self):
        return calendar.timegm(datetime.utcnow().utctimetuple())

    def save(self, patient):
        sequence_number = self._get_sequence_number()

        args = [self.data, sequence_number]
        kwargs = {'patient_id': patient.id}

        logger.info('Adding SDA to queue')

        import_sda.delay(*args, **kwargs)


def _split_names(names):
    return itertools.chain(*[_split_name(x) for x in names])


def _split_name(name):
    name = name.upper()
    name = re.sub('[^A-Z ]', '', name)
    parts = name.split(' ')
    return parts
