from radar.database import db
from radar.models.patients import Patient
from radar.models.patient_demographics import PatientDemographics
from radar.patient_search import filter_by_date_of_birth, filter_by_first_name, \
    filter_by_last_name, filter_by_patient_number
from radar.models.cohorts import CohortPatient
from radar.models.patient_numbers import PatientNumber
from radar.organisations import get_nhs_organisation, get_chi_organisation, \
    get_ukrdc_organisation
from radar.cohorts import get_radar_cohort
from radar.data_sources import get_radar_data_source
from radar.models.organisations import OrganisationPatient


def recruit_patient_search(params):
    query = Patient.query\
        .filter(filter_by_first_name(params['first_name']))\
        .filter(filter_by_last_name(params['last_name']))\
        .filter(filter_by_date_of_birth(params['date_of_birth']))\

    if params.get('patient_number'):
        query = query.filter(filter_by_patient_number(params['patient_number']))

    patients = query.all()

    results = []

    for patient in patients:
        result = {
            'radar_id': patient.id,
            'first_name': patient.first_name,
            'last_name': patient.last_name,
            'date_of_birth': patient.date_of_birth,
        }
        results.append(result)

    return results


def recruit_patient(params):
    radar_id = params.get('radar_id')
    cohort = params['cohort']
    organisation = params['organisation']

    if radar_id:
        patient = Patient.query.get(radar_id)
    else:
        radar_data_source = get_radar_data_source()
        radar_cohort = get_radar_cohort()

        patient = Patient()
        db.session.add(patient)

        radar_cohort_patient = CohortPatient()
        radar_cohort_patient.patient = patient
        radar_cohort_patient.cohort = radar_cohort
        radar_cohort_patient.recruited_by_organisation = organisation
        db.session.add(radar_cohort_patient)

        patient_demographics = PatientDemographics()
        patient_demographics.patient = patient
        patient_demographics.data_source = radar_data_source
        patient_demographics.first_name = params['first_name']
        patient_demographics.last_name = params['last_name']
        patient_demographics.gender = params['gender']
        patient_demographics.ethnicity = params['ethnicity']
        db.session.add(patient_demographics)

        if params.get('mpiid'):
            ukrdc_organisation = get_ukrdc_organisation()
            patient_number = PatientNumber()
            patient_number.patient = patient
            patient_number.data_source = radar_data_source
            patient_number.organisation = ukrdc_organisation
            patient_number.number = params['mpiid']
            db.session.add(patient_number)

        if params.get('nhs_no'):
            nhs_organisation = get_nhs_organisation()
            patient_number = PatientNumber()
            patient_number.patient = patient
            patient_number.data_source = radar_data_source
            patient_number.organisation = nhs_organisation
            patient_number.number = params['nhs_no']
            db.session.add(patient_number)

        if params.get('chi_no'):
            chi_organisation = get_chi_organisation()
            patient_number = PatientNumber()
            patient_number.patient = patient
            patient_number.data_source = radar_data_source
            patient_number.organisation = chi_organisation
            patient_number.number = params['chi_no']
            db.session.add(patient_number)

    if not patient.in_cohort(cohort):
        cohort_patient = CohortPatient()
        cohort_patient.patient = patient
        cohort_patient.cohort = cohort
        cohort_patient.recruited_by_organisation = organisation
        db.session.add(cohort_patient)

    if not patient.in_organisation(organisation):
        organisation_patient = OrganisationPatient()
        organisation_patient.patient = patient
        organisation_patient.organisation = organisation
        db.session.add(organisation_patient)

    db.session.commit()

    return patient
