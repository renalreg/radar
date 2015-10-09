from radar_api.serializers.data_sources import OrganisationSerializer
from radar_api.serializers.meta import MetaSerializerMixin
from radar.serializers.fields import ListField
from radar.serializers.models import ModelSerializer
from radar.models import Consultant


class ConsultantSerializer(MetaSerializerMixin, ModelSerializer):
    organisations = ListField(field=OrganisationSerializer(), read_only=True)

    class Meta(object):
        model_class = Consultant
