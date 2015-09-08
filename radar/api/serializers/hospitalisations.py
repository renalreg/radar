from radar.lib.serializers import MetaSerializerMixin, PatientSerializerMixin, FacilitySerializerMixin, ModelSerializer
from radar.models import Hospitalisation


class HospitalisationSerializer(MetaSerializerMixin, PatientSerializerMixin, FacilitySerializerMixin, ModelSerializer):
    class Meta:
        model_class = Hospitalisation
