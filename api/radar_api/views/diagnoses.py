from radar_api.serializers.diagnoses import DiagnosisSerializer
from radar.models.diagnoses import Diagnosis
from radar.validation.diagnoses import DiagnosisValidation
from radar.views.groups import GroupObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView


class DiagnosisListView(GroupObjectViewMixin, PatientObjectListView):
    serializer_class = DiagnosisSerializer
    validation_class = DiagnosisValidation
    model_class = Diagnosis


class DiagnosisDetailView(GroupObjectViewMixin, PatientObjectDetailView):
    serializer_class = DiagnosisSerializer
    validation_class = DiagnosisValidation
    model_class = Diagnosis


def register_views(app):
    app.add_url_rule('/diagnoses', view_func=DiagnosisListView.as_view('diagnosis_list'))
    app.add_url_rule('/diagnoses/<id>', view_func=DiagnosisDetailView.as_view('diagnosis_detail'))
