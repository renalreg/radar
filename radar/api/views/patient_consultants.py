from radar.api.serializers.consultants import PatientConsultantSerializer
from radar.api.views.common import (
    PatientObjectDetailView,
    PatientObjectListView,
)
from radar.models.patient_consultants import PatientConsultant


class PatientConsultantListView(PatientObjectListView):
    model_class = PatientConsultant
    serializer_class = PatientConsultantSerializer


class PatientConsultantDetailView(PatientObjectDetailView):
    model_class = PatientConsultant
    serializer_class = PatientConsultantSerializer


def register_views(app):
    app.add_url_rule('/patient-consultants', view_func=PatientConsultantListView.as_view('patient_consultant_list'))
    app.add_url_rule(
        '/patient-consultants/<int:id>',
        view_func=PatientConsultantDetailView.as_view('patient_consultant_detail'))
