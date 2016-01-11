from flask import request

from radar.permissions import RadarSourceGroupObjectPermission, SourceGroupObjectPermission
from radar.serializers.core import Serializer
from radar.serializers.fields import IntegerField, StringField


class SourceGroupRequestSerializer(Serializer):
    source_group = IntegerField()
    source = StringField()


class SourceGroupFilterMixin(object):
    def filter_query(self, query):
        query = super(SourceGroupFilterMixin, self).filter_query(query)

        # Note: if a user can view the patient (see PatientObjectViewMixin.filter_query) they can *view* the patient's
        # data from any data source.

        serializer = SourceGroupRequestSerializer()
        args = serializer.to_value(request.args)

        # Filter by source group
        if 'source_group' in args:
            model_class = self.get_model_class()
            query = query.filter(model_class.source_group_id == args['source_group'])

        # Filter by source
        if 'source' in args:
            model_class = self.get_model_class()
            query = query.filter(model_class.source_id == args['source'])

        return query


class SourceGroupObjectViewMixin(SourceGroupFilterMixin):
    def get_permission_classes(self):
        permission_classes = super(SourceGroupObjectViewMixin, self).get_permission_classes()
        permission_classes.append(SourceGroupObjectPermission)
        return permission_classes


class RadarObjectViewMixin(SourceGroupFilterMixin):
    def get_permission_classes(self):
        permission_classes = super(RadarSourceGroupObjectPermission, self).get_permission_classes()
        permission_classes.append(RadarSourceGroupObjectPermission)
        return permission_classes
