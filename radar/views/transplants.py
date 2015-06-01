from flask import Blueprint
from flask_login import current_user
from wtforms import IntegerField

from radar.lib.forms.transplants import TransplantForm
from radar.models.transplants import Transplant
from radar.views.patient_data import PatientDataListAddView, PatientDataListEditView, PatientDataDeleteView, \
    PatientDataListDetailView, PatientDataListView, ListService, DetailService


bp = Blueprint('transplants', __name__)


class TransplantDetailService(DetailService):
    def get_object(self, patient, transplant_id):
        transplant = Transplant.query\
            .filter(Transplant.patient == patient)\
            .filter(Transplant.id == transplant_id)\
            .first_or_404()
        return transplant

    def new_object(self, patient):
        return Transplant(patient=patient)

    def get_form(self, obj):
        class _TransplantForm(TransplantForm):
            pass

        if self.show_apples():
            _TransplantForm.apples = IntegerField()

        return _TransplantForm(obj=obj)

    def show_apples(self):
        return True

    def get_context(self):
        return {
            'show_apples': self.show_apples()
        }


class TransplantListService(ListService):
    def get_objects(self, patient):
        transplants = Transplant.query\
            .filter(Transplant.patient == patient)\
            .order_by(Transplant.transplant_date.desc())\
            .all()
        return transplants


class TransplantListView(PatientDataListView):
    def __init__(self):
        super(TransplantListView, self).__init__(
            TransplantListService(current_user),
        )

    def get_template_name(self):
        return 'patient/transplants.html'


class TransplantListAddView(PatientDataListAddView):
    def __init__(self):
        super(TransplantListAddView, self).__init__(
            TransplantListService(current_user),
            TransplantDetailService(current_user),
        )

    def success_endpoint(self):
        return 'transplants.view_transplant_list'

    def get_template_name(self):
        return 'patient/transplants.html'


class TransplantListDetailView(PatientDataListDetailView):
    def __init__(self):
        super(TransplantListDetailView, self).__init__(
            TransplantListService(current_user),
            TransplantDetailService(current_user),
        )

    def get_template_name(self):
        return 'patient/transplants.html'


class TransplantListEditView(PatientDataListEditView):
    def __init__(self):
        super(TransplantListEditView, self).__init__(
            TransplantListService(current_user),
            TransplantDetailService(current_user),
        )

    def success_endpoint(self):
        return 'transplants.view_transplant_list'

    def get_template_name(self):
        return 'patient/transplants.html'


class TransplantDeleteView(PatientDataDeleteView):
    def __init__(self):
        super(TransplantDeleteView, self).__init__(
            TransplantDetailService(current_user),
        )

    def success_endpoint(self):
        return 'transplants.view_transplant_list'


bp.add_url_rule('/', view_func=TransplantListView.as_view('view_transplant_list'))
bp.add_url_rule('/add/', view_func=TransplantListAddView.as_view('add_transplant'))
bp.add_url_rule('/<int:transplant_id>/', view_func=TransplantListDetailView.as_view('view_transplant'))
bp.add_url_rule('/<int:transplant_id>/edit/', view_func=TransplantListEditView.as_view('edit_transplant'))
bp.add_url_rule('/<int:transplant_id>/delete/', view_func=TransplantDeleteView.as_view('delete_transplant'))