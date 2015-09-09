from radar.lib.serializers import ModelSerializer, MetaSerializerMixin, PatientSerializerMixin, \
    DiseaseGroupSerializerMixin
from radar.models import Genetics


class GeneticsSerializer(PatientSerializerMixin, DiseaseGroupSerializerMixin, MetaSerializerMixin, ModelSerializer):
    class Meta:
        model_class = Genetics
