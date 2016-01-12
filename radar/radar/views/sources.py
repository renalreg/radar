from flask import request

from radar.permissions import RadarSourceObjectPermission, SourceObjectPermission
from radar.serializers.core import Serializer
from radar.serializers.fields import IntegerField, StringField


class SourceRequestSerializer(Serializer):
    source_group = IntegerField()
    source_type = StringField()


class SourceFilterMixin(object):
    def filter_query(self, query):
        query = super(SourceFilterMixin, self).filter_query(query)

        # Note: if a user can view the patient (see PatientObjectViewMixin.filter_query) they can *view* the patient's
        # data from any data source.

        serializer = SourceRequestSerializer()
        args = serializer.to_value(request.args)

        # Filter by source group
        if 'source_group' in args:
            model_class = self.get_model_class()
            query = query.filter(model_class.source_group_id == args['source_group'])

        # Filter by source type
        if 'source_type' in args:
            model_class = self.get_model_class()
            query = query.filter(model_class.source_type_id == args['source_type'])

        return query


class SourceObjectViewMixin(SourceFilterMixin):
    def get_permission_classes(self):
        permission_classes = super(SourceObjectViewMixin, self).get_permission_classes()
        permission_classes.append(SourceObjectPermission)
        return permission_classes


class RadarObjectViewMixin(SourceFilterMixin):
    def get_permission_classes(self):
        permission_classes = super(RadarObjectViewMixin, self).get_permission_classes()
        permission_classes.append(RadarSourceObjectPermission)
        return permission_classes
