from radar.api.serializers.disease_groups import DiseaseGroupSerializer
from radar.lib.views import ListCreateApiView, ListView, RetrieveView
from radar.models import DiseaseGroup


class DiseaseGroupList(ListView):
    serializer_class = DiseaseGroupSerializer
    model_class = DiseaseGroup


class DiseaseGroupDetail(RetrieveView):
    serializer_class = DiseaseGroupSerializer
    model_class = DiseaseGroup
