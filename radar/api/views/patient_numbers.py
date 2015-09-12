from radar.api.serializers.patient_numbers import PatientNumberSerializer
from radar.lib.models import PatientNumber
from radar.lib.validation.patient_numbers import PatientNumberValidation
from radar.lib.views.data_sources import DataSourceObjectViewMixin
from radar.lib.views.patients import PatientObjectDetailView, PatientObjectListView


class PatientNumberListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = PatientNumberSerializer
    model_class = PatientNumber
    validation_class = PatientNumberValidation


class PatientNumberDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = PatientNumberSerializer
    model_class = PatientNumber
    validation_class = PatientNumberValidation
