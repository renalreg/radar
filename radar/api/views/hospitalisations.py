from radar.api.serializers.hospitalisations import HospitalisationSerializer
from radar.lib.views import FacilityDataMixin, PatientDataList, PatientDataDetail
from radar.models import Hospitalisation


class HospitalisationList(FacilityDataMixin, PatientDataList):
    serializer_class = HospitalisationSerializer
    model_class = Hospitalisation


class HospitalisationDetail(FacilityDataMixin, PatientDataDetail):
    serializer_class = HospitalisationSerializer
    model_class = Hospitalisation
