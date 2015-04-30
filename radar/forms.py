from flask import url_for
from radar.database import db
from radar.models import Facility
from radar.sda.models import SDABundle


def save_form_entry(entry):
    sda_bundle = SDABundle()
    sda_bundle.patient = entry.patient
    sda_bundle.facility = Facility.query.filter(Facility.code == 'RADAR').one()

    for concept, _ in entry.to_concepts():
        concept.to_sda(sda_bundle)

    entry.sda_bundle = sda_bundle

    db.session.add(entry)

def delete_form_entry(entry):
    db.session.delete(entry)

def sda_bundle_to_update_url(sda_bundle):
    patient_id = sda_bundle.patient_id
    data_source = sda_bundle.data_source

    if data_source is not None:
        if data_source.type == 'medications':
            return url_for('medication_update', patient_id=patient_id, entry_id=data_source.id)

    return None

def sda_bundle_to_delete_url(sda_bundle):
    patient_id = sda_bundle.patient_id
    data_source = sda_bundle.data_source

    if data_source is not None:
        if data_source.type == 'medications':
            return url_for('medication_delete', patient_id=patient_id, entry_id=data_source.id)

    return None