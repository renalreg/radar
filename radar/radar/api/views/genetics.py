from radar.api.serializers.genetics import GeneticsSerializer
from radar.lib.models import Genetics
from radar.lib.validation.genetics import GeneticsValidation
from radar.lib.views.cohorts import CohortObjectViewMixin
from radar.lib.views.patients import PatientObjectDetailView, PatientObjectListView


class GeneticsListView(CohortObjectViewMixin, PatientObjectListView):
    serializer_class = GeneticsSerializer
    model_class = Genetics
    validation_class = GeneticsValidation


class GeneticsDetailView(CohortObjectViewMixin, PatientObjectDetailView):
    serializer_class = GeneticsSerializer
    model_class = Genetics
    validation_class = GeneticsValidation
