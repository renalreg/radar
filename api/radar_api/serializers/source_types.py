from radar.serializers.models import ModelSerializer, ReferenceField
from radar.models.source_types import SourceType


class SourceTypeSerializer(ModelSerializer):
    class Meta(object):
        model_class = SourceType


class SourceTypeReferenceField(ReferenceField):
    model_class = SourceType
    serializer_class = SourceTypeSerializer
