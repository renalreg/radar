from radar.api.serializers.renal_imaging import RenalImagingSerializer
from radar.lib.models import RenalImaging, RENAL_IMAGING_TYPES, RENAL_IMAGING_KIDNEY_TYPES
from radar.lib.validation.renal_imaging import RenalImagingValidation
from radar.lib.views.codes import CodedStringListView
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


class RenalImagingTypeListView(CodedStringListView):
    items = RENAL_IMAGING_TYPES


class RenalImagingKidneyTypeListView(CodedStringListView):
    items = RENAL_IMAGING_KIDNEY_TYPES
