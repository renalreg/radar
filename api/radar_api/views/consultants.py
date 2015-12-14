from radar_api.serializers.consultants import ConsultantSerializer
from radar.views.core import ListCreateModelView, RetrieveUpdateDestroyModelView
from radar.models import Consultant
from radar.permissions import AdminPermission


class ConsultantListView(ListCreateModelView):
    serializer_class = ConsultantSerializer
    model_class = Consultant
    permission_classes = [AdminPermission]


class ConsultantDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = ConsultantSerializer
    model_class = Consultant
    permission_classes = [AdminPermission]


def register_views(app):
    app.add_url_rule('/consultants', view_func=ConsultantListView.as_view('consultant_list'))
    app.add_url_rule('/consultants/<int:id>', view_func=ConsultantDetailView.as_view('consultant_detail'))
