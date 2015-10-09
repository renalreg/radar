from radar_api.serializers.data_sources import DataSourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.serializers.codes import CodedStringSerializer
from radar.models import Plasmapheresis, PLASMAPHERESIS_RESPONSES, PLASMAPHERESIS_NO_OF_EXCHANGES


class PlasmapheresisSerializer(MetaSerializerMixin, PatientSerializerMixin, DataSourceSerializerMixin, ModelSerializer):
    no_of_exchanges = CodedStringSerializer(PLASMAPHERESIS_NO_OF_EXCHANGES)
    response = CodedStringSerializer(PLASMAPHERESIS_RESPONSES)

    class Meta(object):
        model_class = Plasmapheresis
