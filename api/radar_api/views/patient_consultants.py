from radar_api.serializers.patient_consultants import PatientConsultantSerializer
from radar.models.patient_consultants import PatientConsultant
from radar.views.patients import PatientObjectListView, PatientObjectDetailView
from radar.validation.patient_consultants import PatientConsultantValidation


class PatientConsultantListView(PatientObjectListView):
    model_class = PatientConsultant
    serializer_class = PatientConsultantSerializer
    validation_class = PatientConsultantValidation


class PatientConsultantDetailView(PatientObjectDetailView):
    model_class = PatientConsultant
    serializer_class = PatientConsultantSerializer
    validation_class = PatientConsultantValidation


def register_views(app):
    app.add_url_rule('/patient-consultants', view_func=PatientConsultantListView.as_view('patient_consultant_list'))
    app.add_url_rule('/patient-consultants/<int:id>', view_func=PatientConsultantDetailView.as_view('patient_consultant_detail'))
