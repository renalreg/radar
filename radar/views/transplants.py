from flask import Blueprint

from radar.lib.forms.transplants import TransplantForm
from radar.models.transplants import Transplant
from radar.views.patient_data import PatientDataListAddView, PatientDataListEditView, PatientDataDeleteView, \
    PatientDataListDetailView, PatientDataListView


bp = Blueprint('transplants', __name__)


def get_transplants(patient):
    transplants = Transplant.query\
        .filter(Transplant.patient == patient)\
        .order_by(Transplant.transplant_date.desc())\
        .all()
    return transplants


def get_transplant(patient, transplant_id):
    transplant = Transplant.query\
        .filter(Transplant.patient == patient)\
        .filter(Transplant.id == transplant_id)\
        .first_or_404()
    return transplant


class TransplantListView(PatientDataListView):
    def get_objects(self, patient):
        return get_transplants(patient)

    def get_template_name(self):
        return 'patient/transplants.html'


class TransplantListAddView(PatientDataListAddView):
    def get_objects(self, patient):
        return get_transplants(patient)

    def new_object(self, patient):
        return Transplant(patient=patient)

    def get_form(self, obj):
        return TransplantForm(obj=obj)

    def success_endpoint(self):
        return 'transplants.view_transplant_list'

    def get_template_name(self):
        return 'patient/transplants.html'


class TransplantListDetailView(PatientDataListDetailView):
    def get_object(self, patient, transplant_id):
        return get_transplant(patient, transplant_id)

    def get_objects(self, patient):
        return get_transplants(patient)

    def get_template_name(self):
        return 'patient/transplants.html'


class TransplantListEditView(PatientDataListEditView):
    def get_object(self, patient, transplant_id):
        return get_transplant(patient, transplant_id)

    def get_objects(self, patient):
        return get_transplants(patient)

    def get_form(self, obj):
        return TransplantForm(obj=obj)

    def success_endpoint(self):
        return 'transplants.view_transplant_list'

    def get_template_name(self):
        return 'patient/transplants.html'


class TransplantDeleteView(PatientDataDeleteView):
    def get_object(self, patient, transplant_id):
        return get_transplant(patient, transplant_id)

    def success_endpoint(self):
        return 'transplants.view_transplant_list'


bp.add_url_rule('/', view_func=TransplantListView.as_view('view_transplant_list'))
bp.add_url_rule('/add/', view_func=TransplantListAddView.as_view('add_transplant'))
bp.add_url_rule('/<int:transplant_id>/', view_func=TransplantListDetailView.as_view('view_transplant'))
bp.add_url_rule('/<int:transplant_id>/edit/', view_func=TransplantListEditView.as_view('edit_transplant'))
bp.add_url_rule('/<int:transplant_id>/delete/', view_func=TransplantDeleteView.as_view('delete_transplant'))