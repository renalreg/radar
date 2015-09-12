from flask import request
from radar.lib.permissions import CohortObjectPermission
from radar.lib.serializers import Serializer, IntegerField


class DataSourceRequestSerializer(Serializer):
    data_source = IntegerField()


class DataSourceObjectViewMixin(object):
    def get_permission_classes(self):
        permission_classes = super(DataSourceObjectViewMixin, self).get_permission_classes()
        permission_classes.append(CohortObjectPermission)
        return permission_classes

    def filter_query(self, query):
        query = super(DataSourceObjectViewMixin, self).filter_query(query)

        # Note: if a user can view the patient (see PatientObjectViewMixin.filter_query) they can *view* the patient's
        # data from any data source.

        serializer = DataSourceRequestSerializer()
        args = serializer.to_value(request.args)

        # Filter by data source
        if 'data_source' in args:
            model_class = self.get_model_class()
            query = query.filter(model_class.data_source_id == args['data_source'])

        return query

