from radar.api.serializers.renal_imaging import RenalImagingSerializer
from radar.lib.models import RenalImaging
from radar.lib.validation.renal_imaging import RenalImagingValidation
from radar.lib.views.data_sources import DataSourceObjectViewMixin
from radar.lib.views.patients import PatientObjectDetailView, PatientObjectListView


class RenalImagingListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = RenalImagingSerializer
    model_class = RenalImaging
    validation_class = RenalImagingValidation


class RenalImagingDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = RenalImagingSerializer
    model_class = RenalImaging
    validation_class = RenalImagingValidation
