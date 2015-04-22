import xml.etree.ElementTree as ET
from radar.database import configure_engine, db_session
from radar.models import Facility, SDAContainer, Patient, SDAPatient, SDAImport


def import_sda(facility_code, data):
    facility = Facility.query.filter(Facility.code == facility_code).first()

    root = ET.fromstring(data)

    patient_node = root.find('./Patient')

    mpiid_node = patient_node.find('./MPIID')
    mpiid = mpiid_node.text

    print 'MPIID', mpiid

    radar_id = None

    for patient_number_node in patient_node.findall('./PatientNumbers/PatientNumber'):
        organization_code_node = patient_number_node.find('./Organization/Code')

        if organization_code_node is None:
            continue

        organization_code = organization_code_node.text

        if organization_code == 'RADAR':
            radar_id = int(patient_number_node.find('Number').text)
            break

    print "RADAR ID", radar_id

    patient = Patient.query.get(radar_id)

    sda_container = SDAContainer()
    sda_container.patient = patient
    sda_container.facility = facility
    sda_container.mpiid = mpiid

    sda_patient = SDAPatient()
    sda_patient.name_given_name = patient_node.find('./Name/GivenName').text
    sda_patient.name_family_name = patient_node.find('./Name/FamilyName').text

    sda_container.sda_patient = sda_patient

    sda_import = SDAImport.query.filter(SDAImport.facility == facility, SDAImport.patient == patient).first()

    if sda_import is None:
        sda_import = SDAImport()
        sda_import.facility = facility
        sda_import.patient = patient

    sda_import.sda_container = sda_container

    db_session.add(sda_import)
    db_session.commit()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('facility')
    parser.add_argument('filename')
    args = parser.parse_args()

    configure_engine('postgresql://postgres:password@localhost:5432/radar')

    facility_code = args.facility
    data = open(args.filename, 'rb').read()

    import_sda(facility_code, data)