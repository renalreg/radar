from radar.lib.serializers import MetaSerializerMixin, PatientSerializerMixin, FacilitySerializerMixin, ModelSerializer
from radar.models import PatientAddress


class PatientAddressSerializer(PatientSerializerMixin, FacilitySerializerMixin, MetaSerializerMixin, ModelSerializer):
    class Meta:
        model_class = PatientAddress
