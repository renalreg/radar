from radar_api.serializers.logs import LogSerializer
from radar.models.logs import Log
from radar.permissions import AdminPermission
from radar.views.core import ListModelView, RetrieveModelView


class LogListView(ListModelView):
    serializer_class = LogSerializer
    model_class = Log
    permission_classes = [AdminPermission]


class LogDetailView(RetrieveModelView):
    serializer_class = LogSerializer
    model_class = Log
    permission_classes = [AdminPermission]


def register_views(app):
    app.add_url_rule('/logs', view_func=LogListView.as_view('log_list'))
    app.add_url_rule('/logs/<int:id>', view_func=LogDetailView.as_view('log_detail'))
