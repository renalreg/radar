from radar.api.serializers.data_sources import DataSourceSerializerMixin
from radar.api.serializers.meta import MetaSerializerMixin
from radar.lib.patient_demographics import PatientDemographicsProxy
from radar.lib.serializers.fields import IntegerField
from radar.lib.serializers.models import ModelSerializer, ReferenceField
from radar.lib.serializers.codes import CodedIntegerSerializer
from radar.lib.models import PatientDemographics, EthnicityCode, GENDERS


class EthnicityCodeSerializer(ModelSerializer):
    class Meta(object):
        model_class = EthnicityCode


class EthnicityCodeReferenceField(ReferenceField):
    model_class = EthnicityCode
    serializer_class = EthnicityCodeSerializer


class PatientDemographicsSerializer(MetaSerializerMixin, DataSourceSerializerMixin, ModelSerializer):
    year_of_birth = IntegerField(read_only=True)
    year_of_death = IntegerField(read_only=True)
    ethnicity_code = EthnicityCodeReferenceField()
    gender = CodedIntegerSerializer(GENDERS)

    class Meta(object):
        model_class = PatientDemographics
        exclude = ['ethnicity_code_id']

    def __init__(self, current_user, **kwargs):
        super(PatientDemographicsSerializer, self).__init__(**kwargs)
        self.current_user = current_user

    def to_data(self, value):
        value = PatientDemographicsProxy(value, self.current_user)
        return super(PatientDemographicsSerializer, self).to_data(value)
