from flask.views import View
from flask import redirect, url_for, render_template, request, abort

from radar.database import db_session
from radar.form_services import save_form
from radar.models import Patient
from radar.patients.views import get_patient_detail_context
from radar.form_services import delete_form


class PatientFormList(View):
    model = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get_model_klass(self):
        if self.model is None:
            raise NotImplementedError()

        return self.model

    def dispatch_request(self, patient_id):
        context = get_patient_detail_context(patient_id)

        model_klass = self.get_model_klass()
        forms = model_klass.query.filter(Patient.id == context['patient'].id).all()
        context['forms'] = forms

        return render_template(self.template_name, **context)

class PatientFormDetail(View):
    methods = ['GET', 'POST']
    model = None
    form_handler = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get_model_klass(self):
        if self.model is None:
            raise NotImplementedError()

        return self.model

    def get_form_handler_klass(self):
        if self.form_handler is None:
            raise NotImplementedError()

        return self.form_handler

    def dispatch_request(self, patient_id):
        context = get_patient_detail_context(patient_id)

        patient = context['patient']

        model_klass = self.get_model_klass()
        form_handler_klass = self.get_form_handler_klass()

        form = model_klass.query\
            .with_for_update(read=True)\
            .filter(model_klass.patient == patient)\
            .first()

        if form is None:
            form = model_klass()
            form.patient = patient

        form_handler = form_handler_klass(form)

        if request.method == 'POST':
            form_handler.submit(request.form)

            if form_handler.valid():
                save_form(form)
                db_session.commit()

                return redirect(url_for('.list', patient_id=patient.id))

        context['form'] = form
        context['form_handler'] = form_handler

        return render_template(self.template_name, **context)

class PatientRepeatingFormDetail(View):
    methods = ['GET', 'POST']
    model = None
    form_handler = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get_model_klass(self):
        if self.model is None:
            raise NotImplementedError()

        return self.model

    def get_form_handler_klass(self):
        if self.form_handler is None:
            raise NotImplementedError()

        return self.form_handler

    def dispatch_request(self, patient_id, form_id=None):
        context = get_patient_detail_context(patient_id)

        patient = context['patient']

        model_klass = self.get_model_klass()
        form_handler_klass = self.get_form_handler_klass()

        if form_id is not None:
            form = model_klass.query\
                .with_for_update(read=True)\
                .filter(Patient.id == patient.id, model_klass.id == form_id)\
                .first()

            if form is None:
                abort(404)
        else:
            form = model_klass()
            form.patient = patient

        form_handler = form_handler_klass(form)

        if request.method == 'POST':
            form_handler.submit(request.form)

            if form_handler.valid():
                save_form(form)
                db_session.commit()

                return redirect(url_for('.list', patient_id=patient.id))

        context['form'] = form
        context['form_handler'] = form_handler

        return render_template(self.template_name, **context)

class PatientRepeatingFormDelete(View):
    methods = ['POST']
    model = None

    def get_model_klass(self):
        if self.model is None:
            raise NotImplementedError()

        return self.model

    def dispatch_request(self, patient_id, form_id):
        model_klass = self.get_model_klass()

        form = model_klass.query\
            .with_for_update(read=True)\
            .filter(
                model_klass.patient_id == patient_id,
                model_klass.id == form_id
            )\
            .first()

        if not form:
            abort(404)

        delete_form(form)

        db_session.commit()

        return redirect(url_for('.list', patient_id=patient_id))