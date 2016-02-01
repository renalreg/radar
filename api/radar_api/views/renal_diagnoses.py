from radar_api.serializers.renal_diagnoses import RenalDiagnosisSerializer
from radar.models.renal_diagnoses import RenalDiagnosis
from radar.validation.renal_diagnoses import RenalDiagnosisValidation
from radar.views.patients import PatientObjectDetailView, PatientObjectListView


class RenalDiagnosisListView(PatientObjectListView):
    serializer_class = RenalDiagnosisSerializer
    model_class = RenalDiagnosis
    validation_class = RenalDiagnosisValidation


class RenalDiagnosisDetailView(PatientObjectDetailView):
    serializer_class = RenalDiagnosisSerializer
    model_class = RenalDiagnosis
    validation_class = RenalDiagnosisValidation


def register_views(app):
    app.add_url_rule('/renal-diagnoses', view_func=RenalDiagnosisListView.as_view('renal_diagnosis_list'))
    app.add_url_rule('/renal-diagnoses/<id>', view_func=RenalDiagnosisDetailView.as_view('renal_diagnosis_detail'))
