from radar.api.serializers.genetics import GeneticsSerializer
from radar.api.views.common import (
    IntegerLookupListView,
    GroupObjectViewMixin,
    PatientObjectDetailView,
    PatientObjectListView
)
from radar.models.genetics import Genetics, GENETICS_KARYOTYPES


class GeneticsListView(GroupObjectViewMixin, PatientObjectListView):
    serializer_class = GeneticsSerializer
    model_class = Genetics


class GeneticsDetailView(GroupObjectViewMixin, PatientObjectDetailView):
    serializer_class = GeneticsSerializer
    model_class = Genetics


class GeneticsKaryotypeListView(IntegerLookupListView):
    items = GENETICS_KARYOTYPES


def register_views(app):
    app.add_url_rule('/genetics', view_func=GeneticsListView.as_view('genetics_list'))
    app.add_url_rule('/genetics/<id>', view_func=GeneticsDetailView.as_view('genetics_detail'))
    app.add_url_rule('/genetics-karyotypes', view_func=GeneticsKaryotypeListView.as_view('genetics_karyotype_list'))
