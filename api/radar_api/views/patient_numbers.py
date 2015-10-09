from radar_api.serializers.patient_numbers import PatientNumberSerializer
from radar.models import PatientNumber
from radar.validation.patient_numbers import PatientNumberValidation
from radar.views.data_sources import RadarObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView, DemographicsViewMixin


class PatientNumberListView(RadarObjectViewMixin, DemographicsViewMixin, PatientObjectListView):
    serializer_class = PatientNumberSerializer
    model_class = PatientNumber
    validation_class = PatientNumberValidation


class PatientNumberDetailView(RadarObjectViewMixin, DemographicsViewMixin, PatientObjectDetailView):
    serializer_class = PatientNumberSerializer
    model_class = PatientNumber
    validation_class = PatientNumberValidation
