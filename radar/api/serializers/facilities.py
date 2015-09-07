from radar.lib.serializers import ModelSerializer, MetaSerializerMixin
from radar.models import Facility


class FacilitySerializer(MetaSerializerMixin, ModelSerializer):
    class Meta:
        model_class = Facility
