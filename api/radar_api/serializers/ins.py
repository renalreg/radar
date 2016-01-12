from radar_api.serializers.meta import MetaSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.models.ins import InsClinicalPicture, InsRelapse, KIDNEY_TYPES, REMISSION_TYPES
from radar.serializers.fields import LabelledStringField
from radar_api.serializers.patient_mixins import PatientSerializerMixin


class InsClinicalPictureSerializer(PatientSerializerMixin, MetaSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = InsClinicalPicture


class InsRelapseSerializer(PatientSerializerMixin, MetaSerializerMixin, ModelSerializer):
    kidney_type = LabelledStringField(KIDNEY_TYPES)
    remission_type = LabelledStringField(REMISSION_TYPES)

    class Meta(object):
        model_class = InsRelapse
