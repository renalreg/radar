from radar.api.serializers.dialysis import DialysisSerializer
from radar.api.views.common import (
    IntegerLookupListView,
    PatientObjectDetailView,
    PatientObjectListView,
    SourceObjectViewMixin
)
from radar.models.dialysis import Dialysis, DIALYSIS_MODALITIES


class DialysisListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = DialysisSerializer
    model_class = Dialysis


class DialysisDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = DialysisSerializer
    model_class = Dialysis


class DialysisModalityListView(IntegerLookupListView):
    items = DIALYSIS_MODALITIES


def register_views(app):
    app.add_url_rule('/dialysis', view_func=DialysisListView.as_view('dialysis_list'))
    app.add_url_rule('/dialysis/<id>', view_func=DialysisDetailView.as_view('dialysis_detail'))
    app.add_url_rule('/dialysis-modalities', view_func=DialysisModalityListView.as_view('dialysis_modality_list'))
