from radar_api.serializers.cohorts import CohortSerializer
from radar.views.core import ListModelView, RetrieveModelView
from radar.models import Cohort


class CohortListView(ListModelView):
    serializer_class = CohortSerializer
    model_class = Cohort


class CohortDetailView(RetrieveModelView):
    serializer_class = CohortSerializer
    model_class = Cohort
