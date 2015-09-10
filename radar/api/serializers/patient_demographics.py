from radar.lib.serializers import MetaSerializerMixin, FacilitySerializerMixin, ModelSerializer
from radar.models import PatientDemographics, EthnicityCode


class PatientDemographicsSerializer(MetaSerializerMixin, FacilitySerializerMixin, ModelSerializer):
    class Meta:
        model_class = PatientDemographics


class EthnicityCodeSerializer(ModelSerializer):
    class Meta:
        model_class = EthnicityCode
