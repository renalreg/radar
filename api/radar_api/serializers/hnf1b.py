from radar_api.serializers.meta import MetaSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.models.hnf1b import Hnf1bClinicalPicture
from radar_api.serializers.patient_mixins import PatientSerializerMixin


class Hnf1bClinicalPictureSerializer(PatientSerializerMixin, MetaSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = Hnf1bClinicalPicture
