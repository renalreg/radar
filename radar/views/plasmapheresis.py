from flask import Blueprint, url_for
from flask_login import current_user
from werkzeug.utils import redirect

from radar.lib.forms.plasmapheresis import PlasmapheresisForm
from radar.lib.validation.core import FormErrorHandler
from radar.lib.validation.hospitalisations import validate_hospitalisation
from radar.lib.validation.plasmapheresis import validate_plasmapheresis
from radar.models.plasmapheresis import Plasmapheresis
from radar.views.patient_data import PatientDataListAddView, PatientDataListEditView, PatientDataDeleteView, \
    PatientDataListDetailView, PatientDataListView, ListService, DetailService


bp = Blueprint('plasmapheresis', __name__)


class PlasmapheresisListService(ListService):
    def get_objects(self, patient):
        plasmapheresis_list = Plasmapheresis.query\
            .filter(Plasmapheresis.patient == patient)\
            .order_by(Plasmapheresis.from_date.desc())\
            .all()
        return plasmapheresis_list


class PlasmapheresisDetailService(DetailService):
    def get_object(self, patient, plasmapheresis_id):
        plasmapheresis = Plasmapheresis.query\
            .filter(Plasmapheresis.patient == patient)\
            .filter(Plasmapheresis.id == plasmapheresis_id)\
            .first()
        return plasmapheresis

    def new_object(self, patient):
        return Plasmapheresis(patient=patient)

    def get_form(self, obj):
        return PlasmapheresisForm(obj=obj)

    def validate(self, form, obj):
        errors = FormErrorHandler(form)
        validate_plasmapheresis(errors, obj)
        return errors.is_valid()


class PlasmapheresisListView(PatientDataListView):
    def __init__(self):
        super(PlasmapheresisListView, self).__init__(
            PlasmapheresisListService(current_user),
        )

    def get_template_name(self):
        return 'patient/plasmapheresis.html'


class PlasmapheresisListAddView(PatientDataListAddView):
    def __init__(self):
        super(PlasmapheresisListAddView, self).__init__(
            PlasmapheresisListService(current_user),
            PlasmapheresisDetailService(current_user),
        )

    def saved(self, patient, obj):
        return redirect(url_for('plasmapheresis.view_plasmapheresis_list', patient_id=patient.id))

    def get_template_name(self):
        return 'patient/plasmapheresis.html'


class PlasmapheresisListDetailView(PatientDataListDetailView):
    def __init__(self):
        super(PlasmapheresisListDetailView, self).__init__(
            PlasmapheresisListService(current_user),
            PlasmapheresisDetailService(current_user),
        )

    def get_template_name(self):
        return 'patient/plasmapheresis.html'


class PlasmapheresisListEditView(PatientDataListEditView):
    def __init__(self):
        super(PlasmapheresisListEditView, self).__init__(
            PlasmapheresisListService(current_user),
            PlasmapheresisDetailService(current_user),
        )

    def success_endpoint(self):
        return 'plasmapheresis.view_plasmapheresis_list'

    def get_template_name(self):
        return 'patient/plasmapheresis.html'


class PlasmapheresisDeleteView(PatientDataDeleteView):
    def __init__(self):
        super(PlasmapheresisDeleteView, self).__init__(
            PlasmapheresisDetailService(current_user),
        )

    def deleted(self, patient):
        return redirect(url_for('plasmapheresis.view_plasmapheresis_list', patient_id=patient.id))


bp.add_url_rule('/', view_func=PlasmapheresisListView.as_view('view_plasmapheresis_list'))
bp.add_url_rule('/add/', view_func=PlasmapheresisListAddView.as_view('add_plasmapheresis'))
bp.add_url_rule('/<int:plasmapheresis_id>/', view_func=PlasmapheresisListDetailView.as_view('view_plasmapheresis'))
bp.add_url_rule('/<int:plasmapheresis_id>/edit/', view_func=PlasmapheresisListEditView.as_view('edit_plasmapheresis'))
bp.add_url_rule('/<int:plasmapheresis_id>/delete/', view_func=PlasmapheresisDeleteView.as_view('delete_plasmapheresis'))