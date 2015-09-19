from radar.api.serializers.data_sources import DataSourceSerializerMixin
from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.patient_mixins import PatientSerializerMixin
from radar.lib.serializers.models import ModelSerializer, ReferenceField
from radar.lib.models import DialysisType, Dialysis


class DialysisTypeSerializer(ModelSerializer):
    class Meta(object):
        model_class = DialysisType


class DialysisTypeReferenceField(ReferenceField):
    model_class = DialysisType
    serializer_class = DialysisTypeSerializer


class DialysisSerializer(MetaSerializerMixin, PatientSerializerMixin, DataSourceSerializerMixin, ModelSerializer):
    dialysis_type = DialysisTypeReferenceField()

    class Meta(object):
        model_class = Dialysis
        exclude = ['dialysis_type_id']
