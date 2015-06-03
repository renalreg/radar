from flask import url_for
from flask_login import current_user
from werkzeug.utils import redirect
from radar.lib.facilities import get_radar_facility
from radar.models import PatientAlias
from radar.web.forms.patients import PatientAliasForm
from radar.web.views.patient_data import PatientDataDeleteView, PatientDataEditView, PatientDataAddView, \
    PatientDataDetailService


class PatientAliasDetailService(PatientDataDetailService):
    def get_object(self, patient, patient_alias_id):
        patient_alias = PatientAlias.query\
            .filter(PatientAlias.patient == patient)\
            .filter(PatientAlias.id == patient_alias_id)\
            .first()
        return patient_alias

    def new_object(self, patient):
        return PatientAlias(patient=patient, facility=get_radar_facility())

    def get_form(self, obj):
        return PatientAliasForm(obj=obj)


class PatientAliasAddView(PatientDataAddView):
    def __init__(self):
        super(PatientAliasAddView, self).__init__(
            PatientAliasDetailService(current_user)
        )

    def get_template_name(self):
        return 'patient/patient_alias_form.html'

    def saved(self, patient, obj):
        return redirect(url_for('patients.view_demographics_list', patient_id=patient.id))


class PatientAliasEditView(PatientDataEditView):
    def __init__(self):
        super(PatientAliasEditView, self).__init__(
            PatientAliasDetailService(current_user)
        )

    def get_template_name(self):
        return 'patient/patient_alias_form.html'

    def saved(self, patient, obj):
        return redirect(url_for('patients.view_demographics_list', patient_id=patient.id))


class PatientAliasDeleteView(PatientDataDeleteView):
    def __init__(self):
        super(PatientAliasDeleteView, self).__init__(
            PatientAliasDetailService(current_user)
        )

    def deleted(self, patient):
        return redirect(url_for('patients.view_demographics_list', patient_id=patient.id))


def register_routes(bp):
    bp.add_url_rule('/<int:patient_id>/aliases/add/', view_func=PatientAliasAddView.as_view('add_patient_alias'))
    bp.add_url_rule('/<int:patient_id>/aliases/<int:patient_alias_id>/edit/', view_func=PatientAliasEditView.as_view('edit_patient_alias'))
    bp.add_url_rule('/<int:patient_id>/aliases/<int:patient_alias_id>/delete/', view_func=PatientAliasDeleteView.as_view('delete_patient_alias'))
