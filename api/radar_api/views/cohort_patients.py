from radar_api.serializers.cohort_patients import CohortPatientSerializer
from radar.models import CohortPatient
from radar.validation.cohort_patients import CohortPatientValidation
from radar.views.core import RetrieveUpdateDestroyModelView, ListCreateModelView
from radar.permissions import CohortPatientPermission


class CohortPatientListView(ListCreateModelView):
    serializer_class = CohortPatientSerializer
    model_class = CohortPatient
    validation_class = CohortPatientValidation
    permission_classes = [CohortPatientPermission]


class CohortPatientDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = CohortPatientSerializer
    model_class = CohortPatient
    validation_class = CohortPatientValidation
    permission_classes = [CohortPatientPermission]


def register_views(app):
    app.add_url_rule('/cohort-patients', view_func=CohortPatientListView.as_view('cohort_patient_list'))
    app.add_url_rule('/cohort-patients/<int:id>', view_func=CohortPatientDetailView.as_view('cohort_patient_detail'))
