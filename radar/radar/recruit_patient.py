from datetime import datetime

from flask import current_app
import requests
import pytz

from radar.database import db
from radar.models.patients import Patient
from radar.models.patient_demographics import PatientDemographics
from radar.patient_search import filter_by_patient_number_at_group
from radar.models.groups import GroupPatient, Group, GROUP_TYPE_HOSPITAL
from radar.models.patient_numbers import PatientNumber
from radar.groups import get_radar_group, is_radar_group
from radar.models.source_types import SOURCE_TYPE_RADAR
from radar.serializers.ukrdc import SearchSerializer, ResultListSerializer
from radar.auth.sessions import current_user


def is_ukrdc_search_enabled():
    return current_app.config['UKRDC_SEARCH_ENABLED']


def get_ukrdc_search_url():
    return current_app.config['UKRDC_SEARCH_URL']


def get_ukrdc_search_timeout():
    return current_app.config['UKRDC_SEARCH_TIMEOUT']


def search_patients(params):
    patients = search_radar_patients(params)

    if is_ukrdc_search_enabled():
        ukrdc_patients = search_ukrdc_patients(params)
        patients = merge_patient_lists(patients, ukrdc_patients)

    return patients


def search_ukrdc_patients(params):
    url = get_ukrdc_search_url()
    timeout = get_ukrdc_search_timeout()

    request_data = {
        'name': {
            'given_name': params['first_name'],
            'family_name': params['last_name'],
        },
        'birth_time': params['date_of_birth'],
        'patient_number': {
            'number': params['number'],
            'organization': {
                'code': params['number_group'].code,
            },
        }
    }
    request_serializer = SearchSerializer()
    request_data = request_serializer.to_data(request_data)

    try:
        r = requests.post(url, json=request_data, timeout=timeout)
    except requests.exceptions.Timeout:
        # TODO raise/log error?
        return []

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
            number_group_code = patient_number['organization']['code']
            number_group_code = number_group_code.upper()

            # TODO this won't find NHS numbers
            number_group = Group.query.filter(Group.code == number_group_code, Group.type == GROUP_TYPE_HOSPITAL).first()

            if number_group is not None:
                result['patient_numbers'].append({
                    'number': number,
                    'number_group': number_group,
                })

        results.append(result)

    return results


def search_radar_patients(params):
    number_filter = filter_by_patient_number_at_group(params['number'], params['number_group'])
    patients = Patient.query.filter(number_filter).all()

    results = []

    for patient in patients:
        result = {
            'first_name': patient.first_name,
            'last_name': patient.last_name,
            'date_of_birth': patient.date_of_birth,
            'gender': patient.gender,
            'patient_numbers': [
                {
                    'number': patient.id,
                    'number_group': get_radar_group(),
                },
                {
                    'number': params['number'],
                    'number_group': params['number_group'],
                }
            ]
        }

        results.append(result)

    return results


def merge_patient_lists(a, b):
    c = []
    patient_ids = set()

    for x in a:
        patient_id = get_patient_id(x)
        patient_ids.add(patient_id)
        c.append(x)

    for x in b:
        patient_id = get_patient_id(x)

        if patient_id not in patient_ids:
            c.append(x)

    return c


def get_patient_id(patient):
    for x in patient['patient_numbers']:
        if is_radar_group(x['number_group']):
            return int(x['number'])

    return None


def recruit_patient(params):
    patient_id = get_patient_id(params)
    cohort_group = params['cohort_group']
    hospital_group = params['hospital_group']

    if patient_id:
        patient = Patient.query.get(patient_id)
    else:
        radar_group = get_radar_group()

        patient = Patient()
        patient.created_user = current_user
        patient.modified_user = current_user
        db.session.add(patient)

        radar_group_patient = GroupPatient()
        radar_group_patient.patient = patient
        radar_group_patient.group = radar_group
        radar_group_patient.created_group = hospital_group
        radar_group_patient.from_date = datetime.now(pytz.UTC)
        radar_group_patient.created_user = current_user
        radar_group_patient.modified_user = current_user
        db.session.add(radar_group_patient)

        patient_demographics = PatientDemographics()
        patient_demographics.patient = patient
        patient_demographics.source_group = radar_group
        patient_demographics.source_type = SOURCE_TYPE_RADAR
        patient_demographics.first_name = params['first_name']
        patient_demographics.last_name = params['last_name']
        patient_demographics.date_of_birth = params['date_of_birth']
        patient_demographics.gender = params['gender']
        patient_demographics.ethnicity = params.get('ethnicity')
        patient_demographics.created_user = current_user
        patient_demographics.modified_user = current_user
        db.session.add(patient_demographics)

        for x in params['patient_numbers']:
            patient_number = PatientNumber()
            patient_number.patient = patient
            patient_number.source_group = radar_group
            patient_number.source_type = SOURCE_TYPE_RADAR
            patient_number.number_group = x['number_group']
            patient_number.number = x['number']
            patient_number.created_user = current_user
            patient_number.modified_user = current_user
            db.session.add(patient_number)

    # Add the patient to the cohort group
    if not patient.in_group(cohort_group, current=True):
        cohort_group_patient = GroupPatient()
        cohort_group_patient.patient = patient
        cohort_group_patient.group = cohort_group
        cohort_group_patient.created_group = hospital_group
        cohort_group_patient.from_date = datetime.now(pytz.UTC)
        cohort_group_patient.created_user = current_user
        cohort_group_patient.modified_user = current_user
        db.session.add(cohort_group_patient)

    # Add the patient to the hospital group
    if not patient.in_group(hospital_group, current=True):
        hospital_group_patient = GroupPatient()
        hospital_group_patient.patient = patient
        hospital_group_patient.group = hospital_group
        hospital_group_patient.from_date = datetime.now(pytz.UTC)
        hospital_group_patient.created_user = current_user
        hospital_group_patient.modified_user = current_user
        db.session.add(hospital_group_patient)

    db.session.commit()

    return patient
