from flask import Blueprint

from radar.lib.forms.hospitalisations import HospitalisationForm
from radar.models.hospitalisations import Hospitalisation
from radar.views.patient_data import PatientDataListAddView, PatientDataListEditView, PatientDataDeleteView, \
    PatientDataListDetailView, PatientDataListView


bp = Blueprint('hospitalisations', __name__)


def get_hospitalisations(patient):
    hospitalisations = Hospitalisation.query\
        .filter(Hospitalisation.patient == patient)\
        .order_by(Hospitalisation.date_of_admission.desc())\
        .all()
    return hospitalisations


def get_hospitalisation(patient, hospitalisation_id):
    hospitalisation = Hospitalisation.query\
        .filter(Hospitalisation.patient == patient)\
        .filter(Hospitalisation.id == hospitalisation_id)\
        .with_for_update(read=True)\
        .first_or_404()
    return hospitalisation


class HospitalisationListView(PatientDataListView):
    def get_objects(self, patient):
        return get_hospitalisations(patient)

    def get_template_name(self):
        return 'patient/hospitalisations.html'


class HospitalisationListAddView(PatientDataListAddView):
    def get_objects(self, patient):
        return get_hospitalisations(patient)

    def new_object(self, patient):
        return Hospitalisation(patient=patient)

    def get_form(self, obj):
        return HospitalisationForm(obj=obj)

    def success_endpoint(self):
        return 'hospitalisations.view_hospitalisation_list'

    def get_template_name(self):
        return 'patient/hospitalisations.html'


class HospitalisationListDetailView(PatientDataListDetailView):
    def get_object(self, patient, hospitalisation_id):
        return get_hospitalisation(patient, hospitalisation_id)

    def get_objects(self, patient):
        return get_hospitalisations(patient)

    def get_template_name(self):
        return 'patient/hospitalisations.html'


class HospitalisationListEditView(PatientDataListEditView):
    def get_object(self, patient, hospitalisation_id):
        return get_hospitalisation(patient, hospitalisation_id)

    def get_objects(self, patient):
        return get_hospitalisations(patient)

    def get_form(self, obj):
        return HospitalisationForm(obj=obj)

    def success_endpoint(self):
        return 'hospitalisations.view_hospitalisation_list'

    def get_template_name(self):
        return 'patient/hospitalisations.html'


class HospitalisationDeleteView(PatientDataDeleteView):
    def get_object(self, patient, hospitalisation_id):
        return get_hospitalisation(patient, hospitalisation_id)

    def success_endpoint(self):
        return 'hospitalisations.view_hospitalisation_list'


bp.add_url_rule('/', view_func=HospitalisationListView.as_view('view_hospitalisation_list'))
bp.add_url_rule('/add/', view_func=HospitalisationListAddView.as_view('add_hospitalisation'))
bp.add_url_rule('/<int:hospitalisation_id>/', view_func=HospitalisationListDetailView.as_view('view_hospitalisation'))
bp.add_url_rule('/<int:hospitalisation_id>/edit/', view_func=HospitalisationListEditView.as_view('edit_hospitalisation'))
bp.add_url_rule('/<int:hospitalisation_id>/delete/', view_func=HospitalisationDeleteView.as_view('delete_hospitalisation'))