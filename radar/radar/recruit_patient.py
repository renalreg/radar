from flask import current_app
import requests

from radar.database import db
from radar.models.patients import Patient
from radar.models.patient_demographics import PatientDemographics
from radar.patient_search import filter_by_patient_number_at_organisation
from radar.models.cohorts import CohortPatient
from radar.models.patient_numbers import PatientNumber
from radar.organisations import get_radar_organisation, is_radar_organisation
from radar.cohorts import get_radar_cohort
from radar.data_sources import get_radar_data_source
from radar.models.organisations import OrganisationPatient
from radar.validation.utils import validate
from radar.validation.core import ValidationError
from radar.serializers.ukrdc import SearchSerializer, ResultListSerializer
from radar.models.organisations import Organisation


def is_ukrdc_search_enabled():
    return current_app.config['UKRDC_SEARCH_ENABLED']


def get_ukrdc_search_url():
    return current_app.config['UKRDC_SEARCH_URL']


def search_patients(params):
    patients = search_radar_patients(params)

    if is_ukrdc_search_enabled():
        ukrdc_patients = search_ukrdc_patients(params)
        patients = merge_patient_lists(patients, ukrdc_patients)

    return patients


def search_ukrdc_patients(params):
    url = get_ukrdc_search_url()

    request_data = {
        'name': {
            'given': params['first_name'],
            'family': params['last_name'],
        },
        'birth_time': params['date_of_birth'],
        'patient_number': {
            'number': params['number'],
            'code_system': params['number_organisation'].code
        }
    }
    request_serializer = SearchSerializer()
    request_data = request_serializer.to_data(request_data)

    r = requests.post(url, json=request_data)

    if r.status_code != 200:
        # TODO raise/log error?
        return []

    response_data = r.json()
    response_serializer = ResultListSerializer()
    response_data = response_serializer.to_value(response_data)

    results = []

    for patient in response_data['patients']:
        result = {}
        result['first_name'] = patient['name']['given']
        result['last_name'] = patient['name']['family']
        result['date_of_birth'] = patient['birth_time']
        result['gender'] = patient['gender']
        result['patient_numbers'] = []

        for patient_number in patient['patient_numbers']:
            number = patient_number['number']
            organisation_code = patient_number['code_system']
            organisation_code = organisation_code.upper()
            number_organisation = Organisation.query.filter(Organisation.code == organisation_code).one()

            result['patient_numbers'].append({
                'number': number,
                'organisation': number_organisation,
            })

        results.append(result)

    return results


def search_radar_patients(params):
    number_filter = filter_by_patient_number_at_organisation(params['number'], params['number_organisation'])
    patients = Patient.query.filter(number_filter).all()

    results = []

    for patient in patients:
        first_name_match = False
        last_name_match = False
        date_of_birth_match = False

        for patient_alias in patient.patient_aliases:
            if patient_alias.first_name.upper() == params['first_name'].upper():
                first_name_match = True

            if patient_alias.last_name.upper() == params['last_name'].upper():
                last_name_match = True

        for patient_demographics in patient.patient_demographics:
            if patient_demographics.date_of_birth == params['date_of_birth']:
                date_of_birth_match = True

        # Check supplied demographics match existing demographics
        # This prevents patient enumeration
        if not first_name_match or not last_name_match or not date_of_birth_match:
            raise ValidationError({'number': "Supplied demographics don't match existing demographics for this patient number."})

        result = {
            'first_name': patient.first_name,
            'last_name': patient.last_name,
            'date_of_birth': patient.date_of_birth,
            'gender': patient.gender,
            'patient_numbers': [
                {
                    'number': patient.id,
                    'organisation': get_radar_organisation(),
                },
                {
                    'number': params['number'],
                    'organisation': params['number_organisation'],
                }
            ]
        }
        results.append(result)

    return results


def merge_patient_lists(a, b):
    c = []
    radar_ids = set()

    for x in a:
        radar_id = get_radar_id(x)
        radar_ids.add(radar_id)
        c.append(x)

    for x in b:
        radar_id = get_radar_id(x)

        if radar_id not in radar_ids:
            c.append(x)

    return c


def get_radar_id(patient):
    # Look for a RaDaR ID
    for x in patient['patient_numbers']:
        if is_radar_organisation(x['organisation']):
            return int(x['number'])

    return None


def recruit_patient(params):
    radar_id = get_radar_id(params)
    cohort = params['cohort']
    organisation = params['recruited_by_organisation']

    if radar_id:
        patient = Patient.query.get(radar_id)
    else:
        radar_data_source = get_radar_data_source()
        radar_cohort = get_radar_cohort()

        patient = Patient()
        patient.is_active = True
        patient = validate(patient)
        db.session.add(patient)

        radar_cohort_patient = CohortPatient()
        radar_cohort_patient.patient = patient
        radar_cohort_patient.cohort = radar_cohort
        radar_cohort_patient.recruited_by_organisation = organisation
        radar_cohort_patient.is_active = True
        radar_cohort_patient = validate(radar_cohort_patient)
        db.session.add(radar_cohort_patient)

        patient_demographics = PatientDemographics()
        patient_demographics.patient = patient
        patient_demographics.data_source = radar_data_source
        patient_demographics.first_name = params['first_name']
        patient_demographics.last_name = params['last_name']
        patient_demographics.date_of_birth = params['date_of_birth']
        patient_demographics.gender = params['gender']
        patient_demographics.ethnicity_code = params.get('ethnicity_code')
        patient_demographics = validate(patient_demographics)
        db.session.add(patient_demographics)

        # TODO validation
        for x in params['patient_numbers']:
            patient_number = PatientNumber()
            patient_number.patient = patient
            patient_number.data_source = radar_data_source
            patient_number.organisation = x['organisation']
            patient_number.number = x['number']
            patient_number = validate(patient_number)
            db.session.add(patient_number)

    # Add the patient to the cohort
    if not patient.in_cohort(cohort):
        cohort_patient = CohortPatient()
        cohort_patient.patient = patient
        cohort_patient.cohort = cohort
        cohort_patient.recruited_by_organisation = organisation
        cohort_patient.is_active = True
        cohort_patient = validate(cohort_patient)
        db.session.add(cohort_patient)

    # Add the patient to the organisation
    if not patient.in_organisation(organisation):
        organisation_patient = OrganisationPatient()
        organisation_patient.patient = patient
        organisation_patient.organisation = organisation
        organisation_patient.is_active = True
        organisation_patient = validate(organisation_patient)
        db.session.add(organisation_patient)

    db.session.commit()

    return patient
