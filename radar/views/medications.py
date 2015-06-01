from flask import Blueprint
from flask_login import current_user

from radar.lib.forms.medications import MedicationForm
from radar.lib.validation.core import FormErrorHandler
from radar.lib.validation.medications import validate_medication
from radar.models.medications import Medication
from radar.views.patient_data import PatientDataDeleteView, PatientDataListAddView, PatientDataListEditView, \
    PatientDataListView, ListService, DetailService

bp = Blueprint('medications', __name__)


class MedicationDetailService(DetailService):
    def get_object(self, patient, medication_id):
        medication = Medication.query\
            .filter(Medication.id == medication_id)\
            .filter(Medication.patient == patient)\
            .first_or_404()
        return medication

    def new_object(self, patient):
        return Medication(patient=patient)

    def get_form(self, obj):
        return MedicationForm(obj=obj)

    def validate(self, form, obj):
        errors = FormErrorHandler(form)
        validate_medication(errors, obj)
        return errors.is_valid()


class MedicationListService(ListService):
    def get_objects(self, patient):
        medications = Medication.query\
            .filter(Medication.patient == patient)\
            .order_by(Medication.from_date.desc(), Medication.to_date.desc(), Medication.name.asc())\
            .all()
        return medications


class MedicationListView(PatientDataListView):
    def __init__(self):
        super(MedicationListView, self).__init__(
            MedicationListService(current_user),
        )

    def get_template_name(self):
        return 'patient/medications.html'


class MedicationListAddView(PatientDataListAddView):
    def __init__(self):
        super(MedicationListAddView, self).__init__(
            MedicationListService(current_user),
            MedicationDetailService(current_user),
        )

    def success_endpoint(self):
        return 'medications.view_medication_list'

    def get_template_name(self):
        return 'patient/medications.html'


class MedicationListEditView(PatientDataListEditView):
    def __init__(self):
        super(MedicationListEditView, self).__init__(
            MedicationListService(current_user),
            MedicationDetailService(current_user),
        )

    def success_endpoint(self):
        return 'medications.view_medication_list'

    def get_template_name(self):
        return 'patient/medications.html'


class MedicationDeleteView(PatientDataDeleteView):
    def __init__(self):
        super(MedicationDeleteView, self).__init__(
            MedicationDetailService(current_user),
        )

    def success_endpoint(self):
        return 'medications.view_medication_list'


bp.add_url_rule('/', view_func=MedicationListView.as_view('view_medication_list'))
bp.add_url_rule('/add/', view_func=MedicationListAddView.as_view('add_medication'))
bp.add_url_rule('/<int:medication_id>/edit/', view_func=MedicationListEditView.as_view('edit_medication'))
bp.add_url_rule('/<int:medication_id>/delete/', view_func=MedicationDeleteView.as_view('delete_medication'))
