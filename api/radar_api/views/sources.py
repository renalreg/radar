from radar_api.serializers.sources import SourceSerializer
from radar.views.core import ListModelView, RetrieveModelView
from radar.models.sources import Source


class SourceListView(ListModelView):
    serializer_class = SourceSerializer
    model_class = Source


class SourceDetailView(RetrieveModelView):
    serializer_class = SourceSerializer
    model_class = Source


def register_views(app):
    app.add_url_rule('/sources', view_func=SourceListView.as_view('source_list'))
    app.add_url_rule('/sources/<id>', view_func=SourceDetailView.as_view('source_detail'))
