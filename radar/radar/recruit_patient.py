from datetime import datetime

from flask import current_app
import requests

from radar.database import db
from radar.models.patients import Patient
from radar.models.patient_demographics import PatientDemographics
from radar.patient_search import filter_by_patient_number_at_group
from radar.models.groups import GroupPatient, Group, GROUP_TYPE_HOSPITAL
from radar.models.patient_numbers import PatientNumber
from radar.groups import get_radar_group, is_radar_group
from radar.source_types import get_radar_source_type
from radar.validation.core import ValidationError, validate
from radar.serializers.ukrdc import SearchSerializer, ResultListSerializer


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
            'given': params['first_name'],
            'family': params['last_name'],
        },
        'birth_time': params['date_of_birth'],
        'patient_number': {
            'number': params['number'],
            'code_system': params['number_group'].code
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
            group_code = patient_number['code_system']
            group_code = group_code.upper()
            group = Group.query.filter(Group.code == group_code, Group.type == GROUP_TYPE_HOSPITAL).first()

            if group is not None:
                result['patient_numbers'].append({
                    'number': number,
                    'group': group,
                })

        results.append(result)

    return results


def search_radar_patients(params):
    number_filter = filter_by_patient_number_at_group(params['number'], params['number_group'])
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
                    'group': get_radar_group(),
                },
                {
                    'number': params['number'],
                    'group': params['number_group'],
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
        if is_radar_group(x['group']):
            return int(x['number'])

    return None


def recruit_patient(params):
    radar_id = get_radar_id(params)
    cohort_group = params['cohort_group']
    hospital_group = params['hospital_group']
    recruited_group = params['recruited_group']

    if radar_id:
        patient = Patient.query.get(radar_id)
    else:
        radar_group = get_radar_group()
        radar_source_type = get_radar_source_type()

        patient = Patient()
        patient.is_active = True
        patient = validate(patient)
        db.session.add(patient)

        radar_group_patient = GroupPatient()
        radar_group_patient.patient = patient
        radar_group_patient.group = radar_group
        radar_group_patient.created_group = recruited_group
        radar_group_patient.from_date = datetime.utcnow()
        radar_group_patient = validate(radar_group_patient)
        db.session.add(radar_group_patient)

        patient_demographics = PatientDemographics()
        patient_demographics.patient = patient
        patient_demographics.source_group = radar_group
        patient_demographics.source_type = radar_source_type
        patient_demographics.first_name = params['first_name']
        patient_demographics.last_name = params['last_name']
        patient_demographics.date_of_birth = params['date_of_birth']
        patient_demographics.gender = params['gender']
        patient_demographics.ethnicity = params.get('ethnicity')
        patient_demographics = validate(patient_demographics)
        db.session.add(patient_demographics)

        # TODO validation
        for x in params['patient_numbers']:
            patient_number = PatientNumber()
            patient_number.patient = patient
            patient_number.source_group = radar_group
            patient_number.source_type = radar_source_type
            patient_number.group = x['group']
            patient_number.number = x['number']
            patient_number = validate(patient_number)
            db.session.add(patient_number)

    # Add the patient to the cohort group
    if not patient.in_group(cohort_group):
        cohort_group_patient = GroupPatient()
        cohort_group_patient.patient = patient
        cohort_group_patient.group = cohort_group
        cohort_group_patient.created_group = hospital_group
        cohort_group_patient.from_date = datetime.utcnow()
        cohort_group_patient = validate(cohort_group_patient)
        db.session.add(cohort_group_patient)

    # Add the patient to the hospital group
    if not patient.in_group(hospital_group):
        hospital_group_patient = GroupPatient()
        hospital_group_patient.patient = patient
        hospital_group_patient.group = hospital_group
        hospital_group_patient.from_date = datetime.utcnow()
        hospital_group_patient = validate(hospital_group_patient)
        db.session.add(hospital_group_patient)

    db.session.commit()

    return patient
