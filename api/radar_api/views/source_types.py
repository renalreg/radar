from radar_api.serializers.source_types import SourceTypeSerializer
from radar.views.core import ListModelView, RetrieveModelView
from radar.models.source_types import SourceType


class SourceTypeListView(ListModelView):
    serializer_class = SourceTypeSerializer
    model_class = SourceType


class SourceTypeDetailView(RetrieveModelView):
    serializer_class = SourceTypeSerializer
    model_class = SourceType


def register_views(app):
    app.add_url_rule('/source-types', view_func=SourceTypeListView.as_view('source_type_list'))
    app.add_url_rule('/source-types/<id>', view_func=SourceTypeDetailView.as_view('source_type_detail'))
