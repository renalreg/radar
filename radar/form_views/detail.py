from flask import abort, render_template
from flask.views import View
from radar.database import db_session
from radar.form_services import save_form_entry
from radar.patients.views import get_patient_detail_context


class BaseFormDetail(View):
    methods = ['GET', 'POST']

    def get_entry_class(self):
        raise NotImplementedError()

    def get_entry_query(self, patient):
        entry_class = self.get_entry_class()

        query = db_session.query(entry_class).filter(entry_class.patient == patient)

        return query

    def get_entry(self, patient, **kwargs):
        return NotImplementedError()

    def get_new_entry(self, patient):
        entry = self.get_entry_class()()
        entry.patient = patient
        return entry

    def get_form(self, entry):
        raise NotImplementedError()

    def validate(self, form, entry):
        return True

    def save(self, entry):
        save_form_entry(entry)
        db_session.commit()

    def get_success(self, entry):
        raise NotImplementedError()

    def get_template_name(self):
        raise NotImplementedError()

    def dispatch_request(self, patient_id, **kwargs):
        context = get_patient_detail_context(patient_id)
        patient = context['patient']

        entry = self.get_entry(patient, **kwargs)
        form = self.get_form(entry)

        if form.validate_on_submit():
            form.populate_obj(entry)

            if self.validate(form, entry):
                self.save(entry)
                return self.get_success(entry)

        context['entry'] = entry
        context['form'] = form

        return render_template(self.get_template_name(), **context)


class SingleFormDetail(BaseFormDetail):
    def get_entry(self, patient):
        query = self.get_entry_query(patient)
        entry = query.first()

        if entry is None:
            entry = self.get_new_entry(patient)

        return entry


class RepeatingFormDetail(BaseFormDetail):
    def get_entry_query(self, patient, entry_id):
        entry_class = self.get_entry_class()
        query = super(RepeatingFormDetail, self).get_entry_query(patient)
        query = query.filter(entry_class.id == entry_id)
        return query

    def get_entry(self, patient, **kwargs):
        entry_id = kwargs.get('entry_id')

        if entry_id is None:
            entry = self.get_new_entry(patient)
        else:
            query = self.get_entry_query(patient)
            entry = query.first()

            if entry is None:
                abort(404)

        return entry

