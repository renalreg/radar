from radar_api.serializers.genetics import GeneticsSerializer
from radar.models import Genetics
from radar.validation.genetics import GeneticsValidation
from radar.views.cohorts import CohortObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView


class GeneticsListView(CohortObjectViewMixin, PatientObjectListView):
    serializer_class = GeneticsSerializer
    model_class = Genetics
    validation_class = GeneticsValidation


class GeneticsDetailView(CohortObjectViewMixin, PatientObjectDetailView):
    serializer_class = GeneticsSerializer
    model_class = Genetics
    validation_class = GeneticsValidation


def register_views(app):
    app.add_url_rule('/genetics', view_func=GeneticsListView.as_view('genetics_list'))
    app.add_url_rule('/genetics/<int:id>', view_func=GeneticsDetailView.as_view('genetics_detail'))
