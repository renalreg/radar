from radar.api.serializers.disease_groups import DiseaseGroupSerializer
from radar.lib.views import ListCreateApiView
from radar.models import DiseaseGroup


class DiseaseGroupList(ListCreateApiView):
    serializer_class = DiseaseGroupSerializer
    model_class = DiseaseGroup
