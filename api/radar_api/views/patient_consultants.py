from radar_api.serializers.patient_consultants import PatientConsultantSerializer
from radar.models import PatientConsultant
from radar.views.patients import PatientObjectListView, PatientObjectDetailView


class PatientConsultantListView(PatientObjectListView):
    model_class = PatientConsultant
    serializer_class = PatientConsultantSerializer


class PatientConsultantDetailView(PatientObjectDetailView):
    model_class = PatientConsultant
    serializer_class = PatientConsultantSerializer


def register_views(app):
    app.add_url_rule('/patient-consultants', view_func=PatientConsultantListView.as_view('patient_consultant_list'))
    app.add_url_rule('/patient-consultants/<int:id>', view_func=PatientConsultantDetailView.as_view('patient_consultant_detail'))
