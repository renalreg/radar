from radar.api.serializers.genetics import GeneticsSerializer
from radar.lib.views import PatientDataList, PatientDataDetail, DiseaseGroupDataMixin
from radar.models import Genetics


class GeneticsList(DiseaseGroupDataMixin, PatientDataList):
    serializer_class = GeneticsSerializer
    model_class = Genetics


class GeneticsDetail(DiseaseGroupDataMixin, PatientDataDetail):
    serializer_class = GeneticsSerializer
    model_class = Genetics
