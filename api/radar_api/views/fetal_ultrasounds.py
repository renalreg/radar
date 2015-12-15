from radar_api.serializers.fetal_ultrasounds import FetalUltrasoundSerializer
from radar.models.fetal_ultrasounds import FetalUltrasound, LIQUOR_VOLUMES
from radar.validation.fetal_ultrasounds import FetalUltrasoundValidation
from radar.views.data_sources import DataSourceObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView
from radar.views.codes import CodedIntegerListView


class FetalUltrasoundListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = FetalUltrasoundSerializer
    model_class = FetalUltrasound
    validation_class = FetalUltrasoundValidation


class FetalUltrasoundDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = FetalUltrasoundSerializer
    model_class = FetalUltrasound
    validation_class = FetalUltrasoundValidation


class FetalUltrasoundLiquorVolumeListView(CodedIntegerListView):
    items = LIQUOR_VOLUMES


def register_views(app):
    app.add_url_rule('/fetal-ultrasounds', view_func=FetalUltrasoundListView.as_view('fetal_ultrasounds_list'))
    app.add_url_rule('/fetal-ultrasounds/<id>', view_func=FetalUltrasoundDetailView.as_view('fetal_ultrasounds_detail'))
    app.add_url_rule('/fetal-ultrasound-liquor-volumes', view_func=FetalUltrasoundLiquorVolumeListView.as_view('fetal_ultrasound_liquor_volume_list'))
