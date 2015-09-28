from radar.api.serializers.cohorts import CohortSerializer
from radar.lib.views.core import ListModelView, RetrieveModelView
from radar.lib.models import Cohort


class CohortListView(ListModelView):
    serializer_class = CohortSerializer
    model_class = Cohort


class CohortDetailView(RetrieveModelView):
    serializer_class = CohortSerializer
    model_class = Cohort
