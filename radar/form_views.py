from flask.views import View
from flask import redirect, url_for, render_template, request

from radar.database import db_session
from radar.models import Patient, SDAContainer
from radar.views import get_base_context


class FormListView(View):
    model = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get_model_klass(self):
        if self.model is None:
            raise NotImplementedError()

        return self.model

    def dispatch_request(self, patient_id):
        model_klass = self.get_model_klass()

        patient = Patient.query.filter(Patient.id == patient_id).first()
        form_entries = model_klass.query.filter(Patient.id == patient.id).all()

        context = get_base_context()
        context['patient'] = patient
        context['form_entries'] = form_entries

        return render_template(self.template_name, **context)

class FormDetailView(View):
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

    def dispatch_request(self, patient_id, form_entry_id=None):
        model_klass = self.get_model_klass()
        form_handler_klass = self.get_form_handler_klass()

        patient = Patient.query.filter(Patient.id == patient_id).first()

        if form_entry_id is not None:
            form_entry = model_klass.query.filter(Patient.id == patient.id, model_klass.id == form_entry_id).first()
        else:
            form_entry = model_klass()
            form_entry.patient = patient

        form = form_handler_klass(form_entry)

        if request.method == 'POST':
            form.submit(request.form)

            if form.valid():
                if form_entry.sda_container is None:
                    form_entry.sda_container = SDAContainer()

                sda_container = form_entry.sda_container
                sda_container.sda_medications = []

                for concept, _ in form_entry.to_concepts():
                    concept_sda = concept.to_sda()

                    if 'medications' in concept_sda:
                        sda_container.sda_medications.extend(concept_sda['medications'])

                db_session.add(form_entry)
                db_session.commit()

                return redirect(url_for('.list', patient_id=patient.id))

        context = get_base_context()
        context['patient'] = patient
        context['form_entry'] = form_entry
        context['form'] = form

        return render_template(self.template_name, **context)

class FormDeleteView(View):
    methods = ['POST']
    model = None

    def get_model_klass(self):
        if self.model is None:
            raise NotImplementedError()

        return self.model

    def dispatch_request(self, patient_id, form_entry_id):
        model_klass = self.get_model_klass()

        patient = Patient.query.filter(Patient.id == patient_id).first()
        form_entry = model_klass.query.filter(Patient.id == patient.id, model_klass.id == form_entry_id).first()

        db_session.delete(form_entry)
        db_session.commit()

        return redirect(url_for('.list', patient_id=patient.id))