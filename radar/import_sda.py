import xml.etree.ElementTree as ET

from flask import Flask

from radar.database import db
from radar.models import Facility
from radar.patients.models import Patient
from radar.models import DataImport
from radar.sda.parser import parse_container

class Error(Exception):
    pass

class ImportError(Error):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

def import_sda(facility_code, xml_data):
    root = ET.fromstring(xml_data)

    facility = Facility.query.filter(Facility.code == facility_code).first()

    if facility is None:
        raise ImportError('Facility not found (code="%s")' % facility_code)

    patient_node = root.find('./Patient')

    mpiid_node = patient_node.find('./MPIID')
    mpiid = mpiid_node.text

    print 'MPIID = ', mpiid

    patient_id = None

    for patient_number_node in patient_node.findall('./PatientNumbers/PatientNumber'):
        organization_code_node = patient_number_node.find('./Organization/Code')

        if organization_code_node is None:
            continue

        organization_code = organization_code_node.text

        if organization_code == 'RADAR':
            patient_id = int(patient_number_node.find('Number').text)
            break

    print "patient_id =", patient_id

    patient = Patient.query.get(patient_id)

    if patient is None:
        raise ImportError('Patient not found (id="%s")' % patient_id)

    sda_bundle = parse_container(root)
    sda_bundle.patient = patient
    sda_bundle.facility = facility
    sda_bundle.mpiid = mpiid

    data_import = db.session.query(DataImport)\
        .with_for_update(read=True)\
        .filter(
            DataImport.patient == patient,
            DataImport.facility == facility,
        )\
        .first()

    if data_import is None:
        data_import = DataImport()
        data_import.patient = patient
        data_import.facility = facility

    data_import.sda_bundle = sda_bundle

    sda_bundle.serialize()

    db.session.add(data_import)
    db.session.commit()

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    import radar.users.models

    db.init_app(app)

    return app

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('facility_code')
    parser.add_argument('xml_filename')
    args = parser.parse_args()

    facility_code = args.facility_code
    xml_data = open(args.xml_filename, 'rb').read()

    app = create_app('settings.py')

    with app.app_context():
        import_sda(facility_code, xml_data)