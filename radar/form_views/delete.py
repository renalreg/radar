from flask import abort
from flask.views import View
from flask_login import current_user

from radar.database import db_session
from radar.form_services import delete_form_entry
from radar.services import get_patient_for_user


class RepeatingFormDelete(View):
    methods = ['POST']

    def get_entry_class(self):
        raise NotImplementedError()

    def get_entry_query(self, patient, entry_id):
        entry_class = self.get_entry_class()

        query = db_session.query(entry_class)\
            .filter(entry_class.id == entry_id)\
            .filter(entry_class.patient == patient)

        return query

    def delete(self, entry):
        delete_form_entry(entry)
        db_session.commit()

    def success(self, patient):
        raise NotImplementedError()

    def dispatch_request(self, patient_id, entry_id):
        patient = get_patient_for_user(current_user, patient_id)

        if patient is None:
            abort(404)

        query = self.get_entry_query(patient, entry_id)
        entry = query.first()

        if entry is None:
            abort(404)

        self.delete(entry)

        return self.success(patient)