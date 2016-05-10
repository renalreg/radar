from radar.api.serializers.fetal_anomaly_scans import FetalAnomalyScanSerializer
from radar.api.views.common import (
    PatientObjectDetailView,
    PatientObjectListView,
    SourceObjectViewMixin
)
from radar.models.fetal_anomaly_scans import FetalAnomalyScan


class FetalAnomalyScanListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = FetalAnomalyScanSerializer
    model_class = FetalAnomalyScan


class FetalAnomalyScanDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = FetalAnomalyScanSerializer
    model_class = FetalAnomalyScan


def register_views(app):
    app.add_url_rule('/fetal-anomaly-scans', view_func=FetalAnomalyScanListView.as_view('fetal_anomaly_scan_list'))
    app.add_url_rule('/fetal-anomaly-scans/<id>', view_func=FetalAnomalyScanDetailView.as_view('fetal_anomaly_scan_detail'))
