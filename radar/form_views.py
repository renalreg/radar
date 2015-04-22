from flask.views import View
from flask import redirect, url_for, render_template, request

from radar.database import db_session
from radar.models import Patient, SDAContainer, Facility, SDAForm
from radar.patients.views import get_patient_detail_context


class FormListView(View):
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
        form_entries = model_klass.query.filter(Patient.id == context['patient'].id).all()
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
        context = get_patient_detail_context(patient_id)

        patient = context['patient']

        model_klass = self.get_model_klass()
        form_handler_klass = self.get_form_handler_klass()

        if form_entry_id is not None:
            form_entry = model_klass.query.filter(Patient.id == patient.id, model_klass.id == form_entry_id).first()
        else:
            form_entry = model_klass()
            form_entry.patient = patient

        form = form_handler_klass(form_entry)

        if request.method == 'POST':
            form.submit(request.form)

            if form.valid():
                sda_container = SDAContainer()
                sda_container.patient = patient
                sda_container.facility = Facility.query.first() # TODO

                for concept, _ in form_entry.to_concepts():
                    concept.to_sda(sda_container)

                form_entry.sda_container = sda_container

                db_session.add(form_entry)
                db_session.flush()

                print sda_container.id

                sda_form = SDAForm()
                sda_form.sda_container = sda_container
                sda_form.form_type = 'medications' # TODO
                sda_form.form_id = form_entry.id
                db_session.add(sda_form)

                db_session.commit()

                return redirect(url_for('.list', patient_id=patient.id))

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