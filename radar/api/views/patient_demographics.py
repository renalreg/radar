from radar.api.serializers.patient_demographics import PatientDemographicsSerializer, EthnicityCodeSerializer
from radar.lib.views import FacilityDataMixin, PatientDataList, PatientDataDetail, ListView
from radar.models import PatientDemographics, EthnicityCode


class PatientDemographicsList(FacilityDataMixin, PatientDataList):
    serializer_class = PatientDemographicsSerializer
    model_class = PatientDemographics


class PatientDemographicsDetail(FacilityDataMixin, PatientDataDetail):
    serializer_class = PatientDemographicsSerializer
    model_class = PatientDemographics


class EthnicityCodeList(ListView):
    serializer_class = EthnicityCodeSerializer
    model_class = EthnicityCode
