from radar.api.serializers.fetal_anomaly_scans import FetalAnomalyScanSerializer
from radar.api.views.common import (
    PatientObjectDetailView,
    PatientObjectListView,
    SourceObjectViewMixin,
    StringLookupListView,
)
from radar.models.fetal_anomaly_scans import FetalAnomalyScan

from collections import OrderedDict


class FetalAnomalyScanListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = FetalAnomalyScanSerializer
    model_class = FetalAnomalyScan


class FetalAnomalyScanDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = FetalAnomalyScanSerializer
    model_class = FetalAnomalyScan


class FetalAnomalyImagingTypes(StringLookupListView):
    items = OrderedDict(
        [
            ("USS", "USS"),
            ("MRI", "MRI"),
        ]
    )


def register_views(app):
    app.add_url_rule(
        "/fetal-anomaly-scans",
        view_func=FetalAnomalyScanListView.as_view("fetal_anomaly_scan_list"),
    )
    app.add_url_rule(
        "/fetal-anomaly-scans/<id>",
        view_func=FetalAnomalyScanDetailView.as_view("fetal_anomaly_scan_detail"),
    )
    app.add_url_rule(
        "/fetal-anomaly-imaging-types",
        view_func=FetalAnomalyImagingTypes.as_view("fetal_anomaly_imaging_types"),
    )
