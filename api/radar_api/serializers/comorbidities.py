from radar_api.serializers.sources import SourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer, ReferenceField
from radar.models import Disorder, Comorbidity
from radar.serializers.core import Serializer
from radar.serializers.fields import IntegerField, ListField
from radar_api.serializers.groups import TinyGroupSerializer


class DisorderSerializer(ModelSerializer):
    groups = ListField(TinyGroupSerializer())

    class Meta(object):
        model_class = Disorder


class DisorderReferenceField(ReferenceField):
    model_class = Disorder
    serializer_class = DisorderSerializer


class ComorbiditySerializer(MetaSerializerMixin, PatientSerializerMixin, SourceSerializerMixin, ModelSerializer):
    disorder = DisorderReferenceField()

    class Meta(object):
        model_class = Comorbidity
        exclude = ['disorder_id']


class DisorderRequestSerializer(Serializer):
    group = IntegerField()
