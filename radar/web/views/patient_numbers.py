from flask import url_for, redirect
from flask_login import current_user

from radar.lib.facilities import get_radar_facility
from radar.models.patients import PatientNumber
from radar.web.forms.patients import PatientNumberForm
from radar.web.views.patient_data import PatientDataEditView, PatientDataDetailService, \
    PatientDataDeleteView, PatientDataAddView


class PatientNumberDetailService(PatientDataDetailService):
    def get_object(self, patient, patient_number_id):
        patient_number = PatientNumber.query\
            .filter(PatientNumber.patient == patient)\
            .filter(PatientNumber.id == patient_number_id)\
            .first()
        return patient_number

    def new_object(self, patient):
        return PatientNumber(patient=patient, facility=get_radar_facility())

    def get_form(self, obj):
        return PatientNumberForm(obj=obj)


class PatientNumberAddView(PatientDataAddView):
    def __init__(self):
        super(PatientNumberAddView, self).__init__(
            PatientNumberDetailService(current_user)
        )

    def get_template_name(self):
        return 'patient/patient_number_form.html'

    def saved(self, patient, obj):
        return redirect(url_for('patients.view_demographics_list', patient_id=patient.id))


class PatientNumberEditView(PatientDataEditView):
    def __init__(self):
        super(PatientNumberEditView, self).__init__(
            PatientNumberDetailService(current_user)
        )

    def get_template_name(self):
        return 'patient/patient_number_form.html'

    def saved(self, patient, obj):
        return redirect(url_for('patients.view_demographics_list', patient_id=patient.id))


class PatientNumberDeleteView(PatientDataDeleteView):
    def __init__(self):
        super(PatientNumberDeleteView, self).__init__(
            PatientNumberDetailService(current_user)
        )

    def deleted(self, patient):
        return redirect(url_for('patients.view_demographics_list', patient_id=patient.id))


def register_routes(bp):
    bp.add_url_rule('/<int:patient_id>/numbers/add/', view_func=PatientNumberAddView.as_view('add_patient_number'))
    bp.add_url_rule('/<int:patient_id>/numbers/<int:patient_number_id>/edit/', view_func=PatientNumberEditView.as_view('edit_patient_number'))
    bp.add_url_rule('/<int:patient_id>/numbers/<int:patient_number_id>/delete/', view_func=PatientNumberDeleteView.as_view('delete_patient_number'))
