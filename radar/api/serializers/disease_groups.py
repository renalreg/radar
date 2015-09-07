from radar.lib.serializers import ModelSerializer, MetaSerializerMixin, ListField
from radar.models import DiseaseGroupFeature, DiseaseGroup


class DiseaseGroupFeatureSerializer(ModelSerializer):
    class Meta:
        model_class = DiseaseGroupFeature


class DiseaseGroupSerializer(MetaSerializerMixin, ModelSerializer):
    features = ListField(field=DiseaseGroupFeatureSerializer(), source='disease_group_features')

    class Meta:
        model_class = DiseaseGroup
