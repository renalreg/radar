from collections import defaultdict
from radar.models.facilities import Facility
from radar.models.sync import PatientLatestImport
from radar.models.patients import PatientDemographics, PatientNumber, PatientAlias, PatientAddress


class FacilityPatient(object):
    def __init__(self, facility, patient, demographics=None, numbers=None, aliases=None, addresses=None, latest_import=None):
        if numbers is None:
            numbers = []

        if aliases is None:
            aliases = []

        if addresses is None:
            addresses = []

        self.facility = facility
        self.patient = patient
        self.demographics = demographics
        self.numbers = numbers
        self.aliases = aliases
        self.addresses = addresses
        self.latest_import = latest_import

    def can_edit(self, user):
        return self.facility.is_radar and self.patient.can_edit(user)


def get_facility_patients(patient):
    facility_patient_map = defaultdict(FacilityPatient)
    facility_patients = []

    radar_facility = Facility.query.filter(Facility.code == 'RADAR').one()
    radar_facility_patient = FacilityPatient(radar_facility, patient)
    facility_patient_map[radar_facility] = radar_facility_patient
    facility_patients.append(radar_facility_patient)

    def get_facility_patient(facility):
        facility_patient = facility_patient_map.get(facility)

        if facility_patient is None:
            facility_patient = FacilityPatient(facility, patient)
            facility_patient_map[facility] = facility_patient
            facility_patients.append(facility_patient)

        return facility_patient

    patient_demographics_list = PatientDemographics.query\
        .filter(PatientDemographics.patient == patient)\
        .all()
    patient_numbers = PatientNumber.query\
        .filter(PatientNumber.patient == patient)\
        .all()
    patient_aliases = PatientAlias.query\
        .filter(PatientAlias.patient == patient)\
        .all()
    patient_addresses = PatientAddress.query\
        .filter(PatientAddress.patient == patient)\
        .all()
    patient_latest_imports = PatientLatestImport.query\
        .filter(PatientLatestImport.patient == patient)\
        .all()

    # Demographics
    for patient_demographics in patient_demographics_list:
        facility = patient_demographics.facility
        facility_patient = get_facility_patient(facility)
        facility_patient.demographics = patient_demographics

    # Patient numbers
    for patient_number in patient_numbers:
        facility = patient_number.facility
        facility_patient = get_facility_patient(facility)
        facility_patient.numbers.append(patient_number)

    # Aliases
    for patient_alias in patient_aliases:
        facility = patient_alias.facility
        facility_patient = get_facility_patient(facility)
        facility_patient.aliases.append(patient_alias)

    # Addresses
    for patient_address in patient_addresses:
        facility = patient_address.facility
        facility_patient = get_facility_patient(facility)
        facility_patient.addresses.append(patient_address)

    for patient_latest_import in patient_latest_imports:
        facility = patient_latest_import.facility
        facility_patient = get_facility_patient(facility)
        facility_patient.latest_import = patient_latest_import

    # Show RaDaR first then the other facilities in alphabetical order
    facility_patients = [facility_patients[0]] + sorted(facility_patients[1:], key=lambda x: x.facility.name)

    return facility_patients
