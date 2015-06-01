from flask import url_for, request, flash, render_template
from flask.views import View
from flask_login import current_user
from flask import abort, redirect

from radar.lib.database import db
from radar.lib.forms.common import DeleteForm
from radar.models.patients import Patient
from radar.models.transplants import Transplant
from radar.views.patients import get_patient_data


class ListService(object):
    def __init__(self, user):
        self.user = user

    def get_objects(self, patient):
        raise NotImplementedError

    def get_context(self):
        return {}


class DetailService(object):
    def __init__(self, user):
        self.user = user

    def get_object(self, patient, **kwargs):
        raise NotImplementedError

    def new_object(self, patient):
        raise NotImplementedError

    def get_form(self, obj):
        raise NotImplementedError

    def get_context(self):
        return {}


class PatientDataListView(View):
    methods = ['GET']

    def __init__(self, list_service):
        self.list_service = list_service

    def get_template_name(self):
        raise NotImplementedError

    def dispatch_request(self, patient_id):
        patient = Patient.query.get_or_404(patient_id)

        if not patient.can_view(current_user):
            abort(403)

        objects = self.list_service.get_objects(patient)

        context = dict(
            patient=patient,
            patient_data=get_patient_data(patient),
            objects=objects,
        )

        context.update(self.list_service.get_context())

        return render_template(self.get_template_name(), **context)


class PatientDataListAddView(View):
    methods = ['GET', 'POST']

    def __init__(self, list_service, detail_service):
        self.list_service = list_service
        self.detail_service = detail_service

    def success_endpoint(self):
        raise NotImplementedError

    def get_template_name(self):
        raise NotImplementedError

    def dispatch_request(self, patient_id):
        patient = Patient.query.get_or_404(patient_id)

        if not patient.can_view(current_user):
            abort(403)

        objects = self.list_service.get_objects(patient)

        if patient.can_edit(current_user):
            obj = self.detail_service.new_object(patient)
            form = self.detail_service.get_form(obj)
        else:
            obj = None
            form = None

        if request.method == 'POST':
            if obj is None:
                abort(403)

            if form.validate():
                form.populate_obj(obj)

                db.session.add(obj)
                db.session.commit()
                flash('Saved.', 'success')
                return redirect(url_for(self.success_endpoint(), patient_id=patient_id))

        context = dict(
            patient=patient,
            patient_data=get_patient_data(patient),
            form=form,
            objects=objects,
            object=obj
        )

        context.update(self.list_service.get_context())
        context.update(self.detail_service.get_context())

        return render_template(self.get_template_name(), **context)


class PatientDataListDetailView(View):
    methods = ['GET', 'POST']

    def __init__(self, list_service, detail_service):
        self.list_service = list_service
        self.detail_service = detail_service

    def get_template_name(self):
        raise NotImplementedError

    def dispatch_request(self, patient_id, **kwargs):
        patient = Patient.query.get_or_404(patient_id)

        if not patient.can_view(current_user):
            abort(403)

        objects = self.list_service.get_objects(patient)

        obj = self.detail_service.get_object(patient, **kwargs)

        if not obj.can_view(current_user):
            abort(403)

        context = dict(
            patient=patient,
            patient_data=get_patient_data(patient),
            objects=objects,
            object=obj,
        )

        context.update(self.list_service.get_context())
        context.update(self.detail_service.get_context())

        return render_template(self.get_template_name(), **context)


class PatientDataListEditView(View):
    methods = ['GET', 'POST']

    def __init__(self, list_service, detail_service):
        self.list_service = list_service
        self.detail_service = detail_service

    def success_endpoint(self):
        raise NotImplementedError

    def get_template_name(self):
        raise NotImplementedError

    def dispatch_request(self, patient_id, **kwargs):
        patient = Patient.query.get_or_404(patient_id)

        if not patient.can_view(current_user):
            abort(403)

        objects = self.list_service.get_objects(patient)

        obj = self.detail_service.get_object(patient, **kwargs)

        if not obj.can_edit(current_user):
            abort(403)

        form = self.detail_service.get_form(obj)

        if request.method == 'POST':
            if obj is None:
                abort(403)

            if form.validate():
                form.populate_obj(obj)

                db.session.add(obj)
                db.session.commit()
                flash('Saved.', 'success')
                return redirect(url_for(self.success_endpoint(), patient_id=patient_id))

        context = dict(
            patient=patient,
            patient_data=get_patient_data(patient),
            form=form,
            objects=objects,
            object=obj,
        )

        context.update(self.list_service.get_context())
        context.update(self.detail_service.get_context())

        return render_template(self.get_template_name(), **context)


class PatientDataDeleteView(View):
    methods = ['POST']

    def __init__(self, detail_service):
        self.detail_service = detail_service

    def success_endpoint(self):
        raise NotImplementedError

    def dispatch_request(self, patient_id, **kwargs):
        patient = Patient.query.get_or_404(patient_id)

        obj = self.detail_service.get_object(patient, **kwargs)

        form = DeleteForm()

        if not obj.can_edit(current_user) or not form.validate_on_submit():
            abort(403)

        db.session.delete(obj)
        db.session.commit()

        return redirect(url_for(self.success_endpoint(), patient_id=patient_id))