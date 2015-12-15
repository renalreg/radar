from radar_api.serializers.fetal_ultrasounds import FetalUltrasoundSerializer
from radar.models.fetal_ultrasounds import FetalUltrasound
from radar.validation.fetal_ultrasounds import FetalUltrasoundValidation
from radar.views.data_sources import DataSourceObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView


class FetalUltrasoundListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = FetalUltrasoundSerializer
    model_class = FetalUltrasound
    validation_class = FetalUltrasoundValidation


class FetalUltrasoundDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = FetalUltrasoundSerializer
    model_class = FetalUltrasound
    validation_class = FetalUltrasoundValidation


def register_views(app):
    app.add_url_rule('/fetal-ultrasounds', view_func=FetalUltrasoundListView.as_view('fetal_ultrasounds_list'))
    app.add_url_rule('/fetal-ultrasounds/<id>', view_func=FetalUltrasoundDetailView.as_view('fetal_ultrasounds_detail'))
