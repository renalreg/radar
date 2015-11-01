from radar_api.serializers.dialysis import DialysisSerializer, DialysisTypeSerializer
from radar.validation.dialysis import DialysisValidation
from radar.views.core import ListModelView
from radar.models import Dialysis, DialysisType
from radar.views.data_sources import DataSourceObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView


class DialysisListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = DialysisSerializer
    validation_class = DialysisValidation
    model_class = Dialysis


class DialysisDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = DialysisSerializer
    validation_class = DialysisValidation
    model_class = Dialysis


class DialysisTypeListView(ListModelView):
    serializer_class = DialysisTypeSerializer
    model_class = DialysisType


def register_views(app):
    app.add_url_rule('/dialysis', view_func=DialysisListView.as_view('dialysis_list'))
    app.add_url_rule('/dialysis/<id>', view_func=DialysisDetailView.as_view('dialysis_detail'))
    app.add_url_rule('/dialysis-types', view_func=DialysisTypeListView.as_view('dialysis_type_list'))
