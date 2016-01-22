from radar_api.serializers.meta import MetaSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.models.alport import AlportClinicalPicture, DEAFNESS_OPTIONS
from radar.serializers.fields import LabelledIntegerField
from radar_api.serializers.patient_mixins import PatientSerializerMixin


class AlportClinicalPictureSerializer(PatientSerializerMixin, MetaSerializerMixin, ModelSerializer):
    deafness = LabelledIntegerField(DEAFNESS_OPTIONS)

    class Meta(object):
        model_class = AlportClinicalPicture
