from radar.api.serializers.cohort_patients import CohortPatientSerializer
from radar.lib.models import CohortPatient
from radar.lib.validation.cohort_patients import CohortPatientValidation
from radar.lib.views.core import RetrieveUpdateDestroyModelView, ListCreateModelView


class CohortPatientListView(ListCreateModelView):
    serializer_class = CohortPatientSerializer
    model_class = CohortPatient
    validation_class = CohortPatientValidation


class CohortPatientDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = CohortPatientSerializer
    model_class = CohortPatient
    validation_class = CohortPatientValidation
