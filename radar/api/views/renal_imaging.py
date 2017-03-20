from radar.api.serializers.renal_imaging import RenalImagingSerializer
from radar.api.views.common import (
    PatientObjectDetailView,
    PatientObjectListView,
    SourceObjectViewMixin,
    StringLookupListView,
)
from radar.models.renal_imaging import RENAL_IMAGING_KIDNEY_TYPES, RENAL_IMAGING_TYPES, RenalImaging


class RenalImagingListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = RenalImagingSerializer
    model_class = RenalImaging


class RenalImagingDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = RenalImagingSerializer
    model_class = RenalImaging


class RenalImagingTypeListView(StringLookupListView):
    items = RENAL_IMAGING_TYPES


class RenalImagingKidneyTypeListView(StringLookupListView):
    items = RENAL_IMAGING_KIDNEY_TYPES


def register_views(app):
    app.add_url_rule('/renal-imaging', view_func=RenalImagingListView.as_view('renal_imaging_list'))
    app.add_url_rule('/renal-imaging/<id>', view_func=RenalImagingDetailView.as_view('renal_imaging_detail'))
    app.add_url_rule('/renal-imaging-types', view_func=RenalImagingTypeListView.as_view('renal_imaging_type_list'))
    app.add_url_rule(
        '/renal-imaging-kidney-types',
        view_func=RenalImagingKidneyTypeListView.as_view('renal_imaging_kidney_type_list')
    )
