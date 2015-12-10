from radar_api.serializers.data_sources import DataSourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.models import TYPE_OF_TRANSPLANTS, Transplant
from radar.serializers.models import ModelSerializer
from radar.serializers.codes import CodedStringSerializer


class TransplantSerializer(PatientSerializerMixin, DataSourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    transplant_type = CodedStringSerializer(TYPE_OF_TRANSPLANTS)

    class Meta(object):
        model_class = Transplant
