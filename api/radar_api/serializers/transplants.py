from radar_api.serializers.data_sources import DataSourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.models import TYPES_OF_TRANSPLANT, Transplant
from radar.serializers.models import ModelSerializer
from radar.serializers.codes import CodedIntegerSerializer


class TransplantSerializer(PatientSerializerMixin, DataSourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    type_of_transplant = CodedIntegerSerializer(TYPES_OF_TRANSPLANT)

    class Meta(object):
        model_class = Transplant
