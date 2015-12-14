from radar.serializers.models import ModelSerializer
from radar.models.fetal_anomaly_scans import FetalAnomalyScan
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar_api.serializers.data_sources import DataSourceSerializerMixin


class FetalAnomalyScanSerializer(PatientSerializerMixin, DataSourceSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = FetalAnomalyScan
