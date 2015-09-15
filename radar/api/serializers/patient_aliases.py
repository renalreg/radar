from radar.api.serializers.data_sources import DataSourceSerializerMixin
from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.patients import PatientSerializerMixin
from radar.lib.serializers import ModelSerializer
from radar.lib.models import PatientAlias


class PatientAliasSerializer(PatientSerializerMixin, DataSourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = PatientAlias
