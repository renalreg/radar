from radar_api.serializers.fetal_ultrasounds import FetalUltrasoundSerializer
from radar.models.fetal_ultrasounds import FetalUltrasound, LIQUOR_VOLUMES
from radar.validation.fetal_ultrasounds import FetalUltrasoundValidation
from radar.views.sources import SourceObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView
from radar.views.codes import CodedStringListView


class FetalUltrasoundListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = FetalUltrasoundSerializer
    model_class = FetalUltrasound
    validation_class = FetalUltrasoundValidation


class FetalUltrasoundDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = FetalUltrasoundSerializer
    model_class = FetalUltrasound
    validation_class = FetalUltrasoundValidation


class FetalUltrasoundLiquorVolumeListView(CodedStringListView):
    items = LIQUOR_VOLUMES


def register_views(app):
    app.add_url_rule('/fetal-ultrasounds', view_func=FetalUltrasoundListView.as_view('fetal_ultrasounds_list'))
    app.add_url_rule('/fetal-ultrasounds/<id>', view_func=FetalUltrasoundDetailView.as_view('fetal_ultrasounds_detail'))
    app.add_url_rule('/fetal-ultrasound-liquor-volumes', view_func=FetalUltrasoundLiquorVolumeListView.as_view('fetal_ultrasound_liquor_volume_list'))
