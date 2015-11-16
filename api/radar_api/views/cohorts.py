from radar_api.serializers.cohorts import CohortSerializer
from radar.views.core import ListCreateModelView, RetrieveUpdateDestroyModelView
from radar.models import Cohort
from radar.permissions import AdminWritePermission
from radar.validation.cohorts import CohortValidation


class CohortListView(ListCreateModelView):
    serializer_class = CohortSerializer
    model_class = Cohort
    validation_class = CohortValidation
    permission_classes = [AdminWritePermission]


class CohortDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = CohortSerializer
    model_class = Cohort
    validation_class = CohortValidation
    permission_classes = [AdminWritePermission]


def register_views(app):
    app.add_url_rule('/cohorts', view_func=CohortListView.as_view('cohort_list'))
    app.add_url_rule('/cohorts/<int:id>', view_func=CohortDetailView.as_view('cohort_detail'))
