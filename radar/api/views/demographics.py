from radar.lib.serializers import MetaSerializerMixin, FacilitySerializerMixin, ModelSerializer
from radar.lib.views import FacilityDataMixin, PatientDataList, PatientDataDetail
from radar.models import PatientDemographics


class DemographicsSerializer(MetaSerializerMixin, FacilitySerializerMixin, ModelSerializer):
    class Meta:
        model_class = PatientDemographics


class DemographicsList(FacilityDataMixin, PatientDataList):
    serializer_class = DemographicsSerializer

    def get_query(self):
        return PatientDemographics.query


class DemographicsDetail(FacilityDataMixin, PatientDataDetail):
    serializer_class = DemographicsSerializer

    def get_query(self):
        return PatientDemographics.query



