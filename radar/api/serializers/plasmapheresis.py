from radar.api.serializers.data_sources import DataSourceSerializerMixin
from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.patients import PatientSerializerMixin
from radar.lib.serializers import ModelSerializer, CodedStringSerializer
from radar.lib.models import Plasmapheresis, PLASMAPHERESIS_RESPONSES, PLASMAPHERESIS_NO_OF_EXCHANGES


class PlasmapheresisSerializer(MetaSerializerMixin, PatientSerializerMixin, DataSourceSerializerMixin, ModelSerializer):
    no_of_exchanges = CodedStringSerializer(PLASMAPHERESIS_NO_OF_EXCHANGES)
    response = CodedStringSerializer(PLASMAPHERESIS_RESPONSES)

    class Meta:
        model_class = Plasmapheresis
