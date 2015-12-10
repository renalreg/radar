from radar_api.serializers.meta import MetaSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.models.ins import InsClinicalPicture, InsRelapse, TYPES_OF_KIDNEY, TYPES_OF_REMISSION
from radar.serializers.codes import CodedStringSerializer


class InsClinicalPictureSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = InsClinicalPicture


class InsRelapseSerializer(MetaSerializerMixin, ModelSerializer):
    type_of_kidney = CodedStringSerializer(TYPES_OF_KIDNEY)
    type_of_remission = CodedStringSerializer(TYPES_OF_REMISSION)

    class Meta(object):
        model_class = InsRelapse
