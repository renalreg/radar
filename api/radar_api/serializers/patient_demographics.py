from radar_api.serializers.sources import SourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar.patient_demographics import PatientDemographicsProxy
from radar.serializers.fields import IntegerField
from radar.serializers.models import ModelSerializer
from radar.serializers.fields import LabelledIntegerField, LabelledStringField
from radar.models.patient_demographics import PatientDemographics
from radar.models.patients import GENDERS, ETHNICITIES
from radar_api.serializers.patient_mixins import PatientSerializerMixin


class PatientDemographicsSerializer(PatientSerializerMixin, SourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    year_of_birth = IntegerField(read_only=True)
    year_of_death = IntegerField(read_only=True)
    ethnicity = LabelledStringField(ETHNICITIES)
    gender = LabelledIntegerField(GENDERS)

    class Meta(object):
        model_class = PatientDemographics

    def __init__(self, current_user, **kwargs):
        super(PatientDemographicsSerializer, self).__init__(**kwargs)
        self.current_user = current_user

    def to_data(self, value):
        value = PatientDemographicsProxy(value, self.current_user)
        return super(PatientDemographicsSerializer, self).to_data(value)
