from radar.api.serializers.renal_imaging import RenalImagingSerializer
from radar.lib.views import FacilityDataMixin, PatientDataList, PatientDataDetail
from radar.models import RenalImaging


class RenalImagingList(FacilityDataMixin, PatientDataList):
    serializer_class = RenalImagingSerializer
    model_class = RenalImaging


class RenalImagingDetail(FacilityDataMixin, PatientDataDetail):
    serializer_class = RenalImagingSerializer
    model_class = RenalImaging
