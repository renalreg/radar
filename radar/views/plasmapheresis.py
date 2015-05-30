from flask import Blueprint

from radar.lib.forms.plasmapheresis import PlasmapheresisForm
from radar.models.plasmapheresis import Plasmapheresis
from radar.views.patient_data import PatientDataListAddView, PatientDataListEditView, PatientDataDeleteView, \
    PatientDataListDetailView, PatientDataListView


bp = Blueprint('plasmapheresis', __name__)


def get_plasmapheresis_list(patient):
    plasmapheresis_list = Plasmapheresis.query\
        .filter(Plasmapheresis.patient == patient)\
        .order_by(Plasmapheresis.from_date.desc())\
        .all()
    return plasmapheresis_list


def get_plasmapheresis(patient, plasmapheresis_id):
    plasmapheresis = Plasmapheresis.query\
        .filter(Plasmapheresis.patient == patient)\
        .filter(Plasmapheresis.id == plasmapheresis_id)\
        .first_or_404()
    return plasmapheresis


class PlasmapheresisListView(PatientDataListView):
    def get_objects(self, patient):
        return get_plasmapheresis_list(patient)

    def get_template_name(self):
        return 'patient/plasmapheresis.html'


class PlasmapheresisListAddView(PatientDataListAddView):
    def get_objects(self, patient):
        return get_plasmapheresis_list(patient)

    def new_object(self, patient):
        return Plasmapheresis(patient=patient)

    def get_form(self, obj):
        return PlasmapheresisForm(obj=obj)

    def success_endpoint(self):
        return 'plasmapheresis.view_plasmapheresis_list'

    def get_template_name(self):
        return 'patient/plasmapheresis.html'


class PlasmapheresisListDetailView(PatientDataListDetailView):
    def get_object(self, patient, plasmapheresis_id):
        return get_plasmapheresis(patient, plasmapheresis_id)

    def get_objects(self, patient):
        return get_plasmapheresis_list(patient)

    def get_template_name(self):
        return 'patient/plasmapheresis.html'


class PlasmapheresisListEditView(PatientDataListEditView):
    def get_object(self, patient, plasmapheresis_id):
        return get_plasmapheresis(patient, plasmapheresis_id)

    def get_objects(self, patient):
        return get_plasmapheresis_list(patient)

    def get_form(self, obj):
        return PlasmapheresisForm(obj=obj)

    def success_endpoint(self):
        return 'plasmapheresis.view_plasmapheresis_list'

    def get_template_name(self):
        return 'patient/plasmapheresis.html'


class PlasmapheresisDeleteView(PatientDataDeleteView):
    def get_object(self, patient, plasmapheresis_id):
        return get_plasmapheresis(patient, plasmapheresis_id)

    def success_endpoint(self):
        return 'plasmapheresis.view_plasmapheresis_list'


bp.add_url_rule('/', view_func=PlasmapheresisListView.as_view('view_plasmapheresis_list'))
bp.add_url_rule('/add/', view_func=PlasmapheresisListAddView.as_view('add_plasmapheresis'))
bp.add_url_rule('/<int:plasmapheresis_id>/', view_func=PlasmapheresisListDetailView.as_view('view_plasmapheresis'))
bp.add_url_rule('/<int:plasmapheresis_id>/edit/', view_func=PlasmapheresisListEditView.as_view('edit_plasmapheresis'))
bp.add_url_rule('/<int:plasmapheresis_id>/delete/', view_func=PlasmapheresisDeleteView.as_view('delete_plasmapheresis'))