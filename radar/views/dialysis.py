from flask import Blueprint, url_for
from flask_login import current_user
from werkzeug.utils import redirect
from radar.lib.validation.core import FormErrorHandler
from radar.lib.validation.dialysis import validate_dialysis

from radar.lib.forms.dialysis import DialysisForm
from radar.models.dialysis import Dialysis
from radar.views.patient_data import PatientDataListAddView, PatientDataListEditView, PatientDataDeleteView, \
    PatientDataListDetailView, PatientDataListView, DetailService, ListService


bp = Blueprint('dialysis', __name__)


class DialysisListService(ListService):
    def get_objects(self, patient):
        dialysis_list = Dialysis.query\
            .filter(Dialysis.patient == patient)\
            .order_by(Dialysis.from_date.desc())\
            .all()
        return dialysis_list


class DialysisDetailService(DetailService):
    def get_object(self, patient, dialysis_id):
        dialysis = Dialysis.query\
            .filter(Dialysis.patient == patient)\
            .filter(Dialysis.id == dialysis_id)\
            .first()
        return dialysis

    def new_object(self, patient):
        return Dialysis(patient=patient)

    def get_form(self, obj):
        return DialysisForm(obj=obj)

    def validate(self, form, obj):
        errors = FormErrorHandler(form)
        validate_dialysis(errors, obj)
        return errors.is_valid()


class DialysisListView(PatientDataListView):
    def __init__(self):
        super(DialysisListView, self).__init__(
            DialysisListService(current_user),
        )

    def get_template_name(self):
        return 'patient/dialysis.html'


class DialysisListAddView(PatientDataListAddView):
    def __init__(self):
        super(DialysisListAddView, self).__init__(
            DialysisListService(current_user),
            DialysisDetailService(current_user),
        )

    def saved(self, patient, obj):
        return redirect(url_for('dialysis.view_dialysis_list', patient_id=patient.id))

    def get_template_name(self):
        return 'patient/dialysis.html'


class DialysisListDetailView(PatientDataListDetailView):
    def __init__(self):
        super(DialysisListDetailView, self).__init__(
            DialysisListService(current_user),
            DialysisDetailService(current_user),
        )

    def get_template_name(self):
        return 'patient/dialysis.html'


class DialysisListEditView(PatientDataListEditView):
    def __init__(self):
        super(DialysisListEditView, self).__init__(
            DialysisListService(current_user),
            DialysisDetailService(current_user),
        )

    def success_endpoint(self):
        return 'dialysis.view_dialysis_list'

    def get_template_name(self):
        return 'patient/dialysis.html'


class DialysisDeleteView(PatientDataDeleteView):
    def __init__(self):
        super(DialysisDeleteView, self).__init__(
            DialysisDetailService(current_user),
        )

    def deleted(self, patient):
        return redirect(url_for('dialysis.view_dialysis_list', patient_id=patient.id))


bp.add_url_rule('/', view_func=DialysisListView.as_view('view_dialysis_list'))
bp.add_url_rule('/add/', view_func=DialysisListAddView.as_view('add_dialysis'))
bp.add_url_rule('/<int:dialysis_id>/', view_func=DialysisListDetailView.as_view('view_dialysis'))
bp.add_url_rule('/<int:dialysis_id>/edit/', view_func=DialysisListEditView.as_view('edit_dialysis'))
bp.add_url_rule('/<int:dialysis_id>/delete/', view_func=DialysisDeleteView.as_view('delete_dialysis'))