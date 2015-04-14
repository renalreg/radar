from flask.views import View
from flask import redirect, url_for, render_template, request
from radar.database import db_session
from radar.form_builders import FormBuilder
from radar.models import Patient, SDAContainer


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
        forms = model_klass.query.filter(Patient.id == patient.id).all()
        return render_template(self.template_name, patient=patient, forms=forms)

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

    def dispatch_request(self, patient_id, form_id=None):
        model_klass = self.get_model_klass()
        form_handler_klass = self.get_form_handler_klass()

        patient = Patient.query.filter(Patient.id == patient_id).first()

        if form_id is not None:
            form = model_klass.query.filter(Patient.id == patient.id, model_klass.id == form_id).first()
        else:
            form = model_klass()
            form.patient = patient

        form_handler = form_handler_klass(form)

        if request.method == 'POST':
            form_handler.submit(request.form)

            if form_handler.valid():
                if form.sda_container is None:
                    form.sda_container = SDAContainer()

                sda_container = form.sda_container
                sda_container.sda_medications = []

                for concept, _ in form.to_concepts():
                    concept_sda = concept.to_sda()

                    if 'medications' in concept_sda:
                        sda_container.sda_medications.extend(concept_sda['medications'])

                db_session.add(form)
                db_session.commit()

        form_builder = FormBuilder(form_handler)

        return render_template(self.template_name, patient=patient, form=form, form_builder=form_builder)

class FormDeleteView(View):
    methods = ['POST']
    model = None

    def get_model_klass(self):
        if self.model is None:
            raise NotImplementedError()

        return self.model

    def dispatch_request(self, patient_id, form_id):
        model_klass = self.get_model_klass()

        patient = Patient.query.filter(Patient.id == patient_id).first()
        form = model_klass.query.filter(Patient.id == patient.id, model_klass.id == form_id).first()

        db_session.delete(form)
        db_session.commit()

        return redirect(url_for('.list', patient_id=patient.id))