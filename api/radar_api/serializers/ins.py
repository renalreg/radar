from radar_api.serializers.meta import MetaSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.models.ins import InsClinicalPicture, InsRelapse, KIDNEY_TYPE, REMISSION_TYPE
from radar.serializers.codes import CodedStringSerializer
from radar_api.serializers.patient_mixins import PatientSerializerMixin


class InsClinicalPictureSerializer(PatientSerializerMixin, MetaSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = InsClinicalPicture


class InsRelapseSerializer(PatientSerializerMixin, MetaSerializerMixin, ModelSerializer):
    kidney_type = CodedStringSerializer(KIDNEY_TYPE)
    remission_type = CodedStringSerializer(REMISSION_TYPE)

    class Meta(object):
        model_class = InsRelapse
