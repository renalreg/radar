from radar.api.serializers.pkd import LiverImagingSerializer, LiverSymptomsSerializer
from radar.api.views.common import (
    StringLookupListView,
    SourceObjectViewMixin,
    PatientObjectDetailView,
    PatientObjectListView
)
from radar.models.pkd import LiverImaging, LIVER_IMAGING_TYPES, LiverSymptoms


class LiverImagingListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = LiverImagingSerializer
    model_class = LiverImaging


class LiverImagingDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = LiverImagingSerializer
    model_class = LiverImaging


class LiverImagingTypeListView(StringLookupListView):
    items = LIVER_IMAGING_TYPES


class LiverSymptomsListView(PatientObjectListView):
    serializer_class = LiverSymptomsSerializer
    model_class = LiverSymptoms


class LiverSymptomsDetailView(PatientObjectDetailView):
    serializer_class = LiverSymptomsSerializer
    model_class = LiverSymptoms


def register_views(app):
    app.add_url_rule('/liver-imaging', view_func=LiverImagingListView.as_view('liver_imaging_list'))
    app.add_url_rule('/liver-imaging/<id>', view_func=LiverImagingDetailView.as_view('liver_imaging_detail'))
    app.add_url_rule('/liver-imaging-types', view_func=LiverImagingTypeListView.as_view('liver_imaging_type_list'))

    app.add_url_rule('/liver-symptoms', view_func=LiverSymptomsListView.as_view('liver_symptoms_list'))
    app.add_url_rule('/liver-symptoms/<id>', view_func=LiverSymptomsDetailView.as_view('liver_symptoms_detail'))
