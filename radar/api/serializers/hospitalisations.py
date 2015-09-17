from radar.api.serializers.data_sources import DataSourceSerializerMixin
from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.patient_mixins import PatientSerializerMixin
from radar.lib.serializers import ModelSerializer
from radar.lib.models import Hospitalisation


class HospitalisationSerializer(MetaSerializerMixin, PatientSerializerMixin, DataSourceSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = Hospitalisation
