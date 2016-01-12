from radar_api.serializers.sources import SourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.serializers.fields import LabelledStringField
from radar.models import Plasmapheresis, PLASMAPHERESIS_RESPONSES, PLASMAPHERESIS_NO_OF_EXCHANGES


class PlasmapheresisSerializer(MetaSerializerMixin, PatientSerializerMixin, SourceSerializerMixin, ModelSerializer):
    no_of_exchanges = LabelledStringField(PLASMAPHERESIS_NO_OF_EXCHANGES)
    response = LabelledStringField(PLASMAPHERESIS_RESPONSES)

    class Meta(object):
        model_class = Plasmapheresis
