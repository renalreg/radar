from radar.lib.serializers import MetaSerializerMixin, PatientSerializerMixin, FacilitySerializerMixin, ModelSerializer
from radar.models import PatientNumber


class PatientNumberSerializer(PatientSerializerMixin, FacilitySerializerMixin, MetaSerializerMixin, ModelSerializer):
    class Meta:
        model_class = PatientNumber
