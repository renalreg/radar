from radar.api.serializers.data_sources import DataSourceSerializerMixin
from radar.api.serializers.meta import MetaSerializerMixin
from radar.lib.serializers import ModelSerializer
from radar.lib.models import PatientDemographics, EthnicityCode


class PatientDemographicsSerializer(MetaSerializerMixin, DataSourceSerializerMixin, ModelSerializer):
    class Meta:
        model_class = PatientDemographics


class EthnicityCodeSerializer(ModelSerializer):
    class Meta:
        model_class = EthnicityCode
