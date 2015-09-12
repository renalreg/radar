from radar.api.serializers.data_sources import DataSourceSerializer
from radar.lib.views.core import ListModelView, RetrieveModelView
from radar.lib.models import DataSource


class DataSourceListView(ListModelView):
    serializer_class = DataSourceSerializer
    model_class = DataSource


class DataSourceDetailView(RetrieveModelView):
    serializer_class = DataSourceSerializer
    model_class = DataSource
