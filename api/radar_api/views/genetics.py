from radar_api.serializers.genetics import GeneticsSerializer
from radar.models import Genetics
from radar.validation.genetics import GeneticsValidation, GENETICS_KARYOTYPES
from radar.views.groups import GroupObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView
from radar.views.codes import CodedIntegerListView


class GeneticsListView(GroupObjectViewMixin, PatientObjectListView):
    serializer_class = GeneticsSerializer
    model_class = Genetics
    validation_class = GeneticsValidation


class GeneticsDetailView(GroupObjectViewMixin, PatientObjectDetailView):
    serializer_class = GeneticsSerializer
    model_class = Genetics
    validation_class = GeneticsValidation


class GeneticsKaryotypeListView(CodedIntegerListView):
    items = GENETICS_KARYOTYPES


def register_views(app):
    app.add_url_rule('/genetics', view_func=GeneticsListView.as_view('genetics_list'))
    app.add_url_rule('/genetics/<id>', view_func=GeneticsDetailView.as_view('genetics_detail'))
    app.add_url_rule('/genetics-karyotypes', view_func=GeneticsKaryotypeListView.as_view('genetics_karyotype_list'))
