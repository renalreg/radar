from flask import Blueprint, url_for
from flask_login import current_user
from werkzeug.utils import redirect

from radar.web.forms.renal_imaging import RenalImagingForm
from radar.models.renal_imaging import RenalImaging
from radar.web.views.patient_data import PatientDataDeleteView, \
    PatientDataListView, ListService, DetailService, PatientDataDetailView, PatientDataEditView, PatientDataAddView


bp = Blueprint('renal_imaging', __name__)


class RenalImagingListService(ListService):
    def get_objects(self, patient):
        renal_imaging_list = RenalImaging.query\
            .filter(RenalImaging.patient == patient)\
            .order_by(RenalImaging.date.desc())\
            .all()
        return renal_imaging_list


class RenalImagingDetailService(DetailService):
    def get_object(self, patient, renal_imaging_id):
        renal_imaging = RenalImaging.query\
            .filter(RenalImaging.patient == patient)\
            .filter(RenalImaging.id == renal_imaging_id)\
            .first()
        return renal_imaging

    def new_object(self, patient):
        return RenalImaging(patient=patient)

    def get_form(self, obj):
        return RenalImagingForm(obj=obj)


class RenalImagingListView(PatientDataListView):
    def __init__(self):
        super(RenalImagingListView, self).__init__(
            RenalImagingListService(current_user),
        )

    def get_template_name(self):
        return 'patient/renal_imaging.html'


class RenalImagingAddView(PatientDataAddView):
    def __init__(self):
        super(RenalImagingAddView, self).__init__(
            RenalImagingDetailService(current_user),
        )

    def saved(self, patient, obj):
        return redirect(url_for('renal_imaging.view_renal_imaging_list', patient_id=patient.id))

    def get_template_name(self):
        return 'patient/renal_imaging_form.html'


class RenalImagingDetailView(PatientDataDetailView):
    def __init__(self):
        super(RenalImagingDetailView, self).__init__(
            RenalImagingDetailService(current_user),
        )

    def get_template_name(self):
        return 'patient/renal_imaging_detail.html'


class RenalImagingEditView(PatientDataEditView):
    def __init__(self):
        super(RenalImagingEditView, self).__init__(
            RenalImagingDetailService(current_user),
        )

    def saved(self, patient, obj):
        return redirect(url_for('renal_imaging.view_renal_imaging_list', patient_id=patient.id))

    def get_template_name(self):
        return 'patient/renal_imaging_form.html'


class RenalImagingDeleteView(PatientDataDeleteView):
    def __init__(self):
        super(RenalImagingDeleteView, self).__init__(
            RenalImagingDetailService(current_user),
        )

    def deleted(self, patient):
        return redirect(url_for('renal_imaging.view_renal_imaging_list', patient_id=patient.id))


bp.add_url_rule('/', view_func=RenalImagingListView.as_view('view_renal_imaging_list'))
bp.add_url_rule('/add/', view_func=RenalImagingAddView.as_view('add_renal_imaging'))
bp.add_url_rule('/<int:renal_imaging_id>/', view_func=RenalImagingDetailView.as_view('view_renal_imaging'))
bp.add_url_rule('/<int:renal_imaging_id>/edit/', view_func=RenalImagingEditView.as_view('edit_renal_imaging'))
bp.add_url_rule('/<int:renal_imaging_id>/delete/', view_func=RenalImagingDeleteView.as_view('delete_renal_imaging'))