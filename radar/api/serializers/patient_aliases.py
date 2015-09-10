from radar.lib.serializers import MetaSerializerMixin, PatientSerializerMixin, FacilitySerializerMixin, ModelSerializer
from radar.models import PatientAlias


class PatientAliasSerializer(PatientSerializerMixin, FacilitySerializerMixin, MetaSerializerMixin, ModelSerializer):
    class Meta:
        model_class = PatientAlias
