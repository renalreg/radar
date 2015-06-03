from flask import url_for, redirect
from flask_login import current_user

from radar.lib.facilities import get_radar_facility
from radar.models.patients import PatientAddress
from radar.web.forms.patients import PatientAddressForm
from radar.web.views.patient_data import PatientDataEditView, PatientDataDetailService, \
    PatientDataDeleteView, PatientDataAddView


class PatientAddressDetailService(PatientDataDetailService):
    def get_object(self, patient, patient_address_id):
        patient_address = PatientAddress.query\
            .filter(PatientAddress.patient == patient)\
            .filter(PatientAddress.id == patient_address_id)\
            .first()
        return patient_address

    def new_object(self, patient):
        return PatientAddress(patient=patient, facility=get_radar_facility())

    def get_form(self, obj):
        return PatientAddressForm(obj=obj)


class PatientAddressAddView(PatientDataAddView):
    def __init__(self):
        super(PatientAddressAddView, self).__init__(
            PatientAddressDetailService(current_user)
        )

    def get_template_name(self):
        return 'patient/patient_address_form.html'

    def saved(self, patient, obj):
        return redirect(url_for('patients.view_demographics_list', patient_id=patient.id))


class PatientAddressEditView(PatientDataEditView):
    def __init__(self):
        super(PatientAddressEditView, self).__init__(
            PatientAddressDetailService(current_user)
        )

    def get_template_name(self):
        return 'patient/patient_address_form.html'

    def saved(self, patient, obj):
        return redirect(url_for('patients.view_demographics_list', patient_id=patient.id))


class PatientAddressDeleteView(PatientDataDeleteView):
    def __init__(self):
        super(PatientAddressDeleteView, self).__init__(
            PatientAddressDetailService(current_user)
        )

    def deleted(self, patient):
        return redirect(url_for('patients.view_demographics_list', patient_id=patient.id))


def register_routes(bp):
    bp.add_url_rule('/<int:patient_id>/addresses/add/', view_func=PatientAddressAddView.as_view('add_patient_address'))
    bp.add_url_rule('/<int:patient_id>/addresses/<int:patient_address_id>/edit/', view_func=PatientAddressEditView.as_view('edit_patient_address'))
    bp.add_url_rule('/<int:patient_id>/addresses/<int:patient_address_id>/delete/', view_func=PatientAddressDeleteView.as_view('delete_patient_address'))
