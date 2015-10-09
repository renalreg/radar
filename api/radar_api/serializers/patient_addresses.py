from radar_api.serializers.data_sources import DataSourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.patient_addresses import PatientAddressProxy
from radar.serializers.models import ModelSerializer
from radar.models import PatientAddress


class PatientAddressSerializer(PatientSerializerMixin, DataSourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = PatientAddress

    def __init__(self, current_user, **kwargs):
        super(PatientAddressSerializer, self).__init__(**kwargs)
        self.current_user = current_user

    def to_data(self, value):
        value = PatientAddressProxy(value, self.current_user)
        return super(PatientAddressSerializer, self).to_data(value)
