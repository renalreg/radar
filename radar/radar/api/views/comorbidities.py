from radar.api.serializers.comorbidities import ComorbiditySerializer, DisorderSerializer
from radar.lib.validation.comorbidities import ComorbidityValidation
from radar.lib.views.core import ListModelView
from radar.lib.models import Comorbidity, Disorder
from radar.lib.views.data_sources import DataSourceObjectViewMixin
from radar.lib.views.patients import PatientObjectDetailView, PatientObjectListView


class ComorbidityListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = ComorbiditySerializer
    validation_class = ComorbidityValidation
    model_class = Comorbidity


class ComorbidityDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = ComorbiditySerializer
    validation_class = ComorbidityValidation
    model_class = Comorbidity


class DisorderListView(ListModelView):
    serializer_class = DisorderSerializer
    model_class = Disorder
