from radar_api.serializers.consultants import ConsultantSerializer
from radar.views.core import ListModelView, RetrieveModelView
from radar.models import Consultant


class ConsultantListView(ListModelView):
    serializer_class = ConsultantSerializer
    model_class = Consultant


class ConsultantDetailView(RetrieveModelView):
    serializer_class = ConsultantSerializer
    model_class = Consultant


def register_views(app):
    app.add_url_rule('/consultants', view_func=ConsultantListView.as_view('consultant_list'))
    app.add_url_rule('/consultants/<int:id>', view_func=ConsultantDetailView.as_view('consultant_detail'))
