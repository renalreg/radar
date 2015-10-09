from flask import request
from radar_api.serializers.data_sources import DataSourceSerializer, DataSourceRequestSerializer
from radar.views.core import ListModelView, RetrieveModelView
from radar.models import DataSource, Organisation


class DataSourceListView(ListModelView):
    serializer_class = DataSourceSerializer
    model_class = DataSource

    def filter_query(self, query):
        serializer = DataSourceRequestSerializer()
        args = serializer.args_to_value(request.args)

        query = query.join(DataSource.organisation)

        if 'type' in args:
            query = query.filter(DataSource.type == args['type'])

        if 'organisation_code' in args:
            query = query.filter(Organisation.code == args['organisation_code'])

        if 'organisation_type' in args:
            query = query.filter(Organisation.type == args['organisation_type'])

        return query


class DataSourceDetailView(RetrieveModelView):
    serializer_class = DataSourceSerializer
    model_class = DataSource
