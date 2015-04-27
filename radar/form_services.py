from flask import url_for
from radar.database import db_session
from radar.models import Facility, SDAResource


def save_form_entry(entry):
    sda_resource = SDAResource()
    sda_resource.patient = entry.patient
    sda_resource.facility = Facility.query.filter(Facility.code == 'RADAR').one()

    for concept, _ in entry.to_concepts():
        concept.to_sda(sda_resource)

    entry.sda_resource = sda_resource

    db_session.add(entry)

def delete_form_entry(entry):
    db_session.delete(entry)

def sda_resource_to_edit_url(sda_resource):
    patient_id = sda_resource.patient_id
    data_source = sda_resource.data_source

    if data_source is not None:
        if data_source.type == 'medications':
            return url_for('medications.update', patient_id=patient_id, entry_id=data_source.id)

    return None

def sda_resource_to_delete_url(sda_resource):
    patient_id = sda_resource.patient_id
    data_source = sda_resource.data_source

    if data_source is not None:
        if data_source.type == 'medications':
            return url_for('medications.delete', patient_id=patient_id, entry_id=data_source.id)

    return None