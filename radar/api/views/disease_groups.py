from radar.lib.serializers import MetaSerializerMixin, ModelSerializer
from radar.lib.views import ListCreateApiView
from radar.models import DiseaseGroup


class DiseaseGroupSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta:
        model_class = DiseaseGroup


class DiseaseGroupList(ListCreateApiView):
    serializer_class = DiseaseGroupSerializer
    model_class = DiseaseGroup
