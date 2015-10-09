from radar_api.serializers.patient_consultants import PatientConsultantSerializer
from radar.models import PatientConsultant
from radar.views.patients import PatientObjectListView, PatientObjectDetailView


class PatientConsultantListView(PatientObjectListView):
    model_class = PatientConsultant
    serializer_class = PatientConsultantSerializer


class PatientConsultantDetailView(PatientObjectDetailView):
    model_class = PatientConsultant
    serializer_class = PatientConsultantSerializer
