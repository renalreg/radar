from radar_api.serializers.cohorts import CohortSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.models import Genetics, GENETICS_KARYOTYPES
from radar.serializers.codes import CodedIntegerSerializer


class GeneticsSerializer(PatientSerializerMixin, CohortSerializerMixin, MetaSerializerMixin, ModelSerializer):
    karyotype = CodedIntegerSerializer(GENETICS_KARYOTYPES)

    class Meta(object):
        model_class = Genetics
