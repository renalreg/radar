from radar_api.serializers.cohorts import CohortSerializer
from radar.views.core import ListModelView, RetrieveModelView
from radar.models import Cohort


class CohortListView(ListModelView):
    serializer_class = CohortSerializer
    model_class = Cohort


class CohortDetailView(RetrieveModelView):
    serializer_class = CohortSerializer
    model_class = Cohort


def register_views(app):
    app.add_url_rule('/cohorts', view_func=CohortListView.as_view('cohort_list'))
    app.add_url_rule('/cohorts/<int:id>', view_func=CohortDetailView.as_view('cohort_detail'))
