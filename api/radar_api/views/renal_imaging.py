from radar_api.serializers.renal_imaging import RenalImagingSerializer
from radar.models import RenalImaging, RENAL_IMAGING_TYPES, RENAL_IMAGING_KIDNEY_TYPES
from radar.validation.renal_imaging import RenalImagingValidation
from radar.views.codes import CodedStringListView
from radar.views.sources import SourceObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView


class RenalImagingListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = RenalImagingSerializer
    model_class = RenalImaging
    validation_class = RenalImagingValidation


class RenalImagingDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = RenalImagingSerializer
    model_class = RenalImaging
    validation_class = RenalImagingValidation


class RenalImagingTypeListView(CodedStringListView):
    items = RENAL_IMAGING_TYPES


class RenalImagingKidneyTypeListView(CodedStringListView):
    items = RENAL_IMAGING_KIDNEY_TYPES


def register_views(app):
    app.add_url_rule('/renal-imaging', view_func=RenalImagingListView.as_view('renal_imaging_list'))
    app.add_url_rule('/renal-imaging/<id>', view_func=RenalImagingDetailView.as_view('renal_imaging_detail'))
    app.add_url_rule('/renal-imaging-types', view_func=RenalImagingTypeListView.as_view('renal_imaging_type_list'))
    app.add_url_rule('/renal-imaging-kidney-types', view_func=RenalImagingKidneyTypeListView.as_view('renal_imaging_kidney_type_list'))
