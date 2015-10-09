from radar_api.serializers.comorbidities import ComorbiditySerializer, DisorderSerializer
from radar.validation.comorbidities import ComorbidityValidation
from radar.views.core import ListModelView
from radar.models import Comorbidity, Disorder
from radar.views.data_sources import DataSourceObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView


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
