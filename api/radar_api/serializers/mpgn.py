from radar_api.serializers.meta import MetaSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.models.mpgn import MpgnClinicalPicture
from radar_api.serializers.patient_mixins import PatientSerializerMixin


class MpgnClinicalPictureSerializer(PatientSerializerMixin, MetaSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = MpgnClinicalPicture
