from radar_api.serializers.dialysis import DialysisSerializer
from radar.validation.dialysis import DialysisValidation
from radar.models import Dialysis, TYPES_OF_DIALYSIS
from radar.views.data_sources import DataSourceObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView
from radar.views.codes import CodedIntegerListView


class DialysisListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = DialysisSerializer
    validation_class = DialysisValidation
    model_class = Dialysis


class DialysisDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = DialysisSerializer
    validation_class = DialysisValidation
    model_class = Dialysis


class DialysisTypeListView(CodedIntegerListView):
    items = TYPES_OF_DIALYSIS


def register_views(app):
    app.add_url_rule('/dialysis', view_func=DialysisListView.as_view('dialysis_list'))
    app.add_url_rule('/dialysis/<id>', view_func=DialysisDetailView.as_view('dialysis_detail'))
    app.add_url_rule('/dialysis-types', view_func=DialysisTypeListView.as_view('dialysis_type_list'))
