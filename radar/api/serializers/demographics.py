from radar.lib.serializers import MetaSerializerMixin, FacilitySerializerMixin, ModelSerializer
from radar.models import PatientDemographics


class DemographicsSerializer(MetaSerializerMixin, FacilitySerializerMixin, ModelSerializer):
    class Meta:
        model_class = PatientDemographics
