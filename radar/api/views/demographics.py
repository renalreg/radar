from radar.api.serializers.demographics import DemographicsSerializer
from radar.lib.views import FacilityDataMixin, PatientDataList, PatientDataDetail
from radar.models import PatientDemographics


class DemographicsList(FacilityDataMixin, PatientDataList):
    serializer_class = DemographicsSerializer
    model_class = PatientDemographics


class DemographicsDetail(FacilityDataMixin, PatientDataDetail):
    serializer_class = DemographicsSerializer
    model_class = PatientDemographics
