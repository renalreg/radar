from radar_api.serializers.groups import GroupSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.models import Genetics, GENETICS_KARYOTYPES
from radar.serializers.fields import LabelledIntegerField


class GeneticsSerializer(PatientSerializerMixin, GroupSerializerMixin, MetaSerializerMixin, ModelSerializer):
    karyotype = LabelledIntegerField(GENETICS_KARYOTYPES)

    class Meta(object):
        model_class = Genetics
