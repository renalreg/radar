from flask import url_for, request, flash, render_template
from flask.views import View
from flask_login import current_user
from flask import abort, redirect

from radar.lib.database import db
from radar.lib.forms.common import DeleteForm
from radar.models.patients import Patient
from radar.views.patients import get_patient_data


class PatientDataListAddView(View):
    methods = ['GET', 'POST']

    def get_obj_list(self, patient):
        raise NotImplementedError

    def new_obj(self, patient):
        raise NotImplementedError

    def form_to_obj(self, form, obj):
        raise NotImplementedError

    def get_form(self, obj):
        raise NotImplementedError

    def success_endpoint(self):
        raise NotImplementedError

    def get_context(self, obj_list, obj):
        raise NotImplementedError

    def get_template_name(self):
        raise NotImplementedError

    def dispatch_request(self, patient_id):
        patient = Patient.query.get_or_404(patient_id)

        if not patient.can_view(current_user):
            abort(403)

        obj_list = self.get_obj_list(patient)

        if patient.can_edit(current_user):
            obj = self.new_obj(patient)
            form = self.get_form(obj)
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
        )
        context.update(self.get_context(obj_list, obj))

        return render_template(self.get_template_name(), **context)


class PatientDataListEditView(View):
    methods = ['GET', 'POST']

    def get_obj(self, patient, **kwargs):
        raise NotImplementedError

    def get_obj_list(self, patient):
        raise NotImplementedError

    def form_to_obj(self, form, obj):
        raise NotImplementedError

    def get_form(self, obj):
        raise NotImplementedError

    def success_endpoint(self):
        raise NotImplementedError

    def get_context(self, obj_list, obj):
        raise NotImplementedError

    def get_template_name(self):
        raise NotImplementedError

    def dispatch_request(self, patient_id, **kwargs):
        patient = Patient.query.get_or_404(patient_id)

        if not patient.can_view(current_user):
            abort(403)

        obj_list = self.get_obj_list(patient)

        obj = self.get_obj(patient, **kwargs)

        if not obj.can_edit(current_user):
            abort(403)

        form = self.get_form(obj)

        if form.validate_on_submit():
            self.form_to_obj(form, obj)

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
        )
        context.update(self.get_context(obj_list, obj))

        return render_template(self.get_template_name(), **context)


class PatientDataDeleteView(View):
    methods = ['POST']

    def get_obj(self, patient_id, **kwargs):
        raise NotImplementedError

    def success_endpoint(self):
        raise NotImplementedError

    def dispatch_request(self, patient_id, **kwargs):
        patient = Patient.query.get_or_404(patient_id)

        obj = self.get_obj(patient, **kwargs)

        form = DeleteForm()

        if not obj.can_edit(current_user) or not form.validate_on_submit():
            abort(403)

        db.session.delete(obj)
        db.session.commit()

        return redirect(url_for(self.success_endpoint(), patient_id=patient_id))