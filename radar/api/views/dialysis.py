from radar.lib.serializers import MetaSerializerMixin, FacilitySerializerMixin, ModelSerializer, IntegerField
from radar.lib.views import FacilityDataMixin, PatientDataList, PatientDataDetail, ListModelMixin, GenericApiView, \
    ListView
from radar.models import Dialysis, DialysisType

class DialysisTypeSerializer(ModelSerializer):
    class Meta:
        model = DialysisType


class DialysisSerializer(MetaSerializerMixin, FacilitySerializerMixin, ModelSerializer):
    dialysis_type = DialysisTypeSerializer(read_only=True)
    dialysis_type_id = IntegerField(write_only=True)

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


class DialysisTypeList(ListView):
    serializer_class = DialysisTypeSerializer

    def get_query(self):
        return DialysisType.query
