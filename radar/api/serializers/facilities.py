from radar.lib.serializers import ModelSerializer, MetaSerializerMixin
from radar.lib.models import DataSource


class DataSourceSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta:
        model_class = DataSource
