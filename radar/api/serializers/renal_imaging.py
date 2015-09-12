from radar.api.serializers.data_sources import DataSourceSerializerMixin
from radar.api.serializers.meta import MetaSerializerMixin
from radar.lib.serializers import ModelSerializer
from radar.lib.models import RenalImaging


class RenalImagingSerializer(MetaSerializerMixin, DataSourceSerializerMixin, ModelSerializer):
    class Meta:
        model_class = RenalImaging
