from flask import Blueprint, url_for
from flask_login import current_user
from werkzeug.utils import redirect

from radar.web.forms.hospitalisations import HospitalisationForm
from radar.lib.validation.core import FormErrorHandler
from radar.lib.validation.hospitalisations import validate_hospitalisation
from radar.models.hospitalisations import Hospitalisation
from radar.web.views.patient_data import PatientDataListAddView, PatientDataListEditView, PatientDataDeleteView, \
    PatientDataListDetailView, PatientDataListView, DetailService, ListService


bp = Blueprint('hospitalisations', __name__)


class HospitalisationDetailService(DetailService):
    def get_object(self, patient, hospitalisation_id):
        hospitalisation = Hospitalisation.query\
            .filter(Hospitalisation.patient == patient)\
            .filter(Hospitalisation.id == hospitalisation_id)\
            .first()
        return hospitalisation

    def new_object(self, patient):
        return Hospitalisation(patient=patient)

    def get_form(self, obj):
        return HospitalisationForm(obj=obj)

    def validate(self, form, obj):
        errors = FormErrorHandler(form)
        validate_hospitalisation(errors, obj)
        return errors.is_valid()


class HospitalisationListService(ListService):
    def get_objects(self, patient):
        hospitalisations = Hospitalisation.query\
            .filter(Hospitalisation.patient == patient)\
            .order_by(Hospitalisation.date_of_admission.desc())\
            .all()
        return hospitalisations


class HospitalisationListView(PatientDataListView):
    def __init__(self):
        super(HospitalisationListView, self).__init__(
            HospitalisationListService(current_user),
        )

    def get_template_name(self):
        return 'patient/hospitalisations.html'


class HospitalisationListAddView(PatientDataListAddView):
    def __init__(self):
        super(HospitalisationListAddView, self).__init__(
            HospitalisationListService(current_user),
            HospitalisationDetailService(current_user),
        )

    def saved(self, patient, obj):
        return redirect(url_for('hospitalisations.view_hospitalisation_list', patient_id=patient.id))

    def get_template_name(self):
        return 'patient/hospitalisations.html'


class HospitalisationListDetailView(PatientDataListDetailView):
    def __init__(self):
        super(HospitalisationListDetailView, self).__init__(
            HospitalisationListService(current_user),
            HospitalisationDetailService(current_user),
        )

    def get_template_name(self):
        return 'patient/hospitalisations.html'


class HospitalisationListEditView(PatientDataListEditView):
    def __init__(self):
        super(HospitalisationListEditView, self).__init__(
            HospitalisationListService(current_user),
            HospitalisationDetailService(current_user),
        )

    def success_endpoint(self):
        return 'hospitalisations.view_hospitalisation_list'

    def get_template_name(self):
        return 'patient/hospitalisations.html'


class HospitalisationDeleteView(PatientDataDeleteView):
    def __init__(self):
        super(HospitalisationDeleteView, self).__init__(
            HospitalisationDetailService(current_user),
        )

    def deleted(self, patient):
        return redirect(url_for('hospitalisations.view_hospitalisation_list', patient_id=patient.id))


bp.add_url_rule('/', view_func=HospitalisationListView.as_view('view_hospitalisation_list'))
bp.add_url_rule('/add/', view_func=HospitalisationListAddView.as_view('add_hospitalisation'))
bp.add_url_rule('/<int:hospitalisation_id>/', view_func=HospitalisationListDetailView.as_view('view_hospitalisation'))
bp.add_url_rule('/<int:hospitalisation_id>/edit/', view_func=HospitalisationListEditView.as_view('edit_hospitalisation'))
bp.add_url_rule('/<int:hospitalisation_id>/delete/', view_func=HospitalisationDeleteView.as_view('delete_hospitalisation'))