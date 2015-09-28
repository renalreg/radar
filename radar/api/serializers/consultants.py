from radar.api.serializers.data_sources import OrganisationSerializer
from radar.api.serializers.meta import MetaSerializerMixin
from radar.lib.serializers.fields import ListField
from radar.lib.serializers.models import ModelSerializer
from radar.lib.models import Consultant


class ConsultantSerializer(MetaSerializerMixin, ModelSerializer):
    organisations = ListField(field=OrganisationSerializer(), read_only=True)

    class Meta(object):
        model_class = Consultant
