from flask import Blueprint

from radar.lib.forms.dialysis import DialysisForm
from radar.models.dialysis import Dialysis
from radar.views.patient_data import PatientDataListAddView, PatientDataListEditView, PatientDataDeleteView, \
    PatientDataListDetailView, PatientDataListView


bp = Blueprint('dialysis', __name__)


def get_dialysis_list(patient):
    dialysis_list = Dialysis.query\
        .filter(Dialysis.patient == patient)\
        .order_by(Dialysis.from_date.desc())\
        .all()
    return dialysis_list


def get_dialysis(patient, dialysis_id):
    dialysis = Dialysis.query\
        .filter(Dialysis.patient == patient)\
        .filter(Dialysis.id == dialysis_id)\
        .first_or_404()
    return dialysis


class DialysisListView(PatientDataListView):
    def get_objects(self, patient):
        return get_dialysis_list(patient)

    def get_template_name(self):
        return 'patient/dialysis.html'


class DialysisListAddView(PatientDataListAddView):
    def get_objects(self, patient):
        return get_dialysis_list(patient)

    def new_object(self, patient):
        return Dialysis(patient=patient)

    def get_form(self, obj):
        return DialysisForm(obj=obj)

    def success_endpoint(self):
        return 'dialysis.view_dialysis_list'

    def get_template_name(self):
        return 'patient/dialysis.html'


class DialysisListDetailView(PatientDataListDetailView):
    def get_object(self, patient, dialysis_id):
        return get_dialysis(patient, dialysis_id)

    def get_objects(self, patient):
        return get_dialysis_list(patient)

    def get_template_name(self):
        return 'patient/dialysis.html'


class DialysisListEditView(PatientDataListEditView):
    def get_object(self, patient, dialysis_id):
        return get_dialysis(patient, dialysis_id)

    def get_objects(self, patient):
        return get_dialysis_list(patient)

    def get_form(self, obj):
        return DialysisForm(obj=obj)

    def success_endpoint(self):
        return 'dialysis.view_dialysis_list'

    def get_template_name(self):
        return 'patient/dialysis.html'


class DialysisDeleteView(PatientDataDeleteView):
    def get_object(self, patient, dialysis_id):
        return get_dialysis(patient, dialysis_id)

    def success_endpoint(self):
        return 'dialysis.view_dialysis_list'


bp.add_url_rule('/', view_func=DialysisListView.as_view('view_dialysis_list'))
bp.add_url_rule('/add/', view_func=DialysisListAddView.as_view('add_dialysis'))
bp.add_url_rule('/<int:dialysis_id>/', view_func=DialysisListDetailView.as_view('view_dialysis'))
bp.add_url_rule('/<int:dialysis_id>/edit/', view_func=DialysisListEditView.as_view('edit_dialysis'))
bp.add_url_rule('/<int:dialysis_id>/delete/', view_func=DialysisDeleteView.as_view('delete_dialysis'))