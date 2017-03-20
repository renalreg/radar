from radar.api.serializers.fetal_ultrasounds import FetalUltrasoundSerializer
from radar.api.views.common import (
    PatientObjectDetailView,
    PatientObjectListView,
    SourceObjectViewMixin,
    StringLookupListView,
)
from radar.models.fetal_ultrasounds import FetalUltrasound, LIQUOR_VOLUMES


class FetalUltrasoundListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = FetalUltrasoundSerializer
    model_class = FetalUltrasound


class FetalUltrasoundDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = FetalUltrasoundSerializer
    model_class = FetalUltrasound


class FetalUltrasoundLiquorVolumeListView(StringLookupListView):
    items = LIQUOR_VOLUMES


def register_views(app):
    app.add_url_rule('/fetal-ultrasounds', view_func=FetalUltrasoundListView.as_view('fetal_ultrasounds_list'))
    app.add_url_rule('/fetal-ultrasounds/<id>', view_func=FetalUltrasoundDetailView.as_view('fetal_ultrasounds_detail'))
    app.add_url_rule(
        '/fetal-ultrasound-liquor-volumes',
        view_func=FetalUltrasoundLiquorVolumeListView.as_view('fetal_ultrasound_liquor_volume_list')
    )
