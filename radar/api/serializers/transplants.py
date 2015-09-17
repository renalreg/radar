from radar.api.serializers.data_sources import DataSourceSerializerMixin
from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.patient_mixins import PatientSerializerMixin
from radar.lib.models import TRANSPLANT_TYPES, Transplant
from radar.lib.serializers import ModelSerializer, CodedStringSerializer


class TransplantSerializer(PatientSerializerMixin, DataSourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    transplant_type = CodedStringSerializer(TRANSPLANT_TYPES)

    class Meta(object):
        model_class = Transplant
