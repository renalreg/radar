from radar.lib.serializers import MetaSerializerMixin, FacilitySerializerMixin, ModelSerializer
from radar.lib.views import FacilityDataMixin, PatientDataList, PatientDataDetail
from radar.models import Dialysis


class DialysisSerializer(MetaSerializerMixin, FacilitySerializerMixin, ModelSerializer):
    class Meta:
        model = Dialysis


class DialysisList(FacilityDataMixin, PatientDataList):
    serializer_class = DialysisSerializer

    def get_query(self):
        return Dialysis.query


class DialysisDetail(FacilityDataMixin, PatientDataDetail):
    serializer_class = DialysisSerializer

    def get_query(self):
        return Dialysis.query
