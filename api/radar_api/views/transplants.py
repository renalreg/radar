from radar_api.serializers.transplants import TransplantSerializer
from radar.models import TRANSPLANT_TYPES, Transplant
from radar.validation.transplants import TransplantValidation
from radar.views.codes import CodedStringListView
from radar.views.data_sources import DataSourceObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView


class TransplantListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = TransplantSerializer
    model_class = Transplant
    validation_class = TransplantValidation


class TransplantDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = TransplantSerializer
    model_class = Transplant
    validation_class = TransplantValidation


class TransplantTypeListView(CodedStringListView):
    items = TRANSPLANT_TYPES
