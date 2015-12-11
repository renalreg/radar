from radar.serializers.models import ModelSerializer
from radar.models.fetal_anomaly_scans import FetalAnomalyScan


class FetalAnomalyScanSerializer(ModelSerializer):
    class Meta(object):
        model_class = FetalAnomalyScan
