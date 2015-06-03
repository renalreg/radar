from flask import url_for, redirect
from flask_login import current_user

from radar.web.forms.patients import PatientActiveForm
from radar.web.views.patient_data import PatientDataEditView, PatientDataEditService


class PatientActiveEditService(PatientDataEditService):
    def get_object(self, patient):
        return patient

    def get_form(self, obj):
        return PatientActiveForm(obj=obj)


class PatientActiveEditView(PatientDataEditView):
    def __init__(self):
        super(PatientActiveEditView, self).__init__(
            PatientActiveEditService(current_user)
        )

    def get_template_name(self):
        return 'patient/patient_active_form.html'

    def saved(self, patient, obj):
        return redirect(url_for('patients.view_demographics_list', patient_id=patient.id))


def register_routes(bp):
    bp.add_url_rule('/<int:patient_id>/active/', view_func=PatientActiveEditView.as_view('edit_patient_active'))
