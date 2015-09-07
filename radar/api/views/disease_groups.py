from radar.lib.serializers import MetaSerializerMixin, ModelSerializer, ListField
from radar.lib.views import ListCreateApiView
from radar.models import DiseaseGroup, DiseaseGroupFeature


class DiseaseGroupFeatureSerializer(ModelSerializer):
    class Meta:
        model_class = DiseaseGroupFeature


class DiseaseGroupSerializer(MetaSerializerMixin, ModelSerializer):
    features = ListField(field=DiseaseGroupFeatureSerializer(), source='disease_group_features')

    class Meta:
        model_class = DiseaseGroup


class DiseaseGroupList(ListCreateApiView):
    serializer_class = DiseaseGroupSerializer
    model_class = DiseaseGroup
