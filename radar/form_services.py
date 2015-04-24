from radar.database import db_session
from radar.models import FormSDAResource, Facility, SDAResource


def save_form(form):
    db_session.add(form)
    db_session.flush()

    sda_resource = SDAResource()
    sda_resource.patient = form.patient
    sda_resource.facility = Facility.query.filter(Facility.code == 'RADAR').one()

    for concept, _ in form.to_concepts():
        concept.to_sda(sda_resource)

    save_form_sda_resource(form, sda_resource)

def save_form_sda_resource(form, sda_resource):
    form_sda_resource = db_session.query(FormSDAResource)\
        .filter(
            FormSDAResource.form_id == form.id,
            FormSDAResource.form_type == form.__tablename__
        )\
        .first()

    if form_sda_resource is None:
        form_sda_resource = FormSDAResource()
        form_sda_resource.form_id = form.id
        form_sda_resource.form_type = form.__tablename__
    else:
        if form_sda_resource.sda_resource is not None:
            db_session.delete(form_sda_resource.sda_resource)

    form_sda_resource.sda_resource = sda_resource
    db_session.add(form_sda_resource)

def delete_form(form):
    db_session.delete(form)

    form_sda_resource = db_session.query(FormSDAResource)\
        .filter(
            FormSDAResource.form_id == form.id,
            FormSDAResource.form_type == form.__tablename__,
        )\
        .first()

    if form_sda_resource is not None:
        db_session.delete(form_sda_resource)

        if form_sda_resource.sda_resource is not None:
            db_session.delete(form_sda_resource.sda_resource)