from radar.api.serializers.transplants import TransplantSerializer
from radar.lib.models import TRANSPLANT_TYPES, Transplant
from radar.lib.validation.transplants import TransplantValidation
from radar.lib.views.codes import CodedStringListView
from radar.lib.views.data_sources import DataSourceObjectViewMixin
from radar.lib.views.patients import PatientObjectDetailView, PatientObjectListView


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
