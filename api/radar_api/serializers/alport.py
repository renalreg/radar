from radar_api.serializers.meta import MetaSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.models.alport import AlportClinicalPicture, DEAFNESS_OPTIONS
from radar.serializers.codes import CodedIntegerSerializer
from radar_api.serializers.patient_mixins import PatientSerializerMixin


class AlportClinicalPictureSerializer(PatientSerializerMixin, MetaSerializerMixin, ModelSerializer):
    deafness = CodedIntegerSerializer(DEAFNESS_OPTIONS)

    class Meta(object):
        model_class = AlportClinicalPicture
