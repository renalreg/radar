from radar.api.serializers.dialysis import DialysisSerializer, DialysisTypeSerializer
from radar.lib.validation.dialysis import DialysisValidation
from radar.lib.views.core import ListModelView
from radar.lib.models import Dialysis, DialysisType
from radar.lib.views.data_sources import DataSourceObjectViewMixin
from radar.lib.views.patients import PatientObjectDetailView, PatientObjectListView


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
