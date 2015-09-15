from radar.api.serializers.cohorts import CohortSerializerMixin
from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.patients import PatientSerializerMixin
from radar.lib.serializers import ModelSerializer
from radar.lib.models import Genetics


class GeneticsSerializer(PatientSerializerMixin, CohortSerializerMixin, MetaSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = Genetics
