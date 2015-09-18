from flask import request
from radar.api.serializers.organisations import OrganisationSerializer, OrganisationRequestSerializer
from radar.lib.views.core import ListModelView, RetrieveModelView
from radar.lib.models import Organisation


class OrganisationListView(ListModelView):
    serializer_class = OrganisationSerializer
    model_class = Organisation

    def filter_query(self, query):
        serializer = OrganisationRequestSerializer()
        args = serializer.args_to_value(request.args)

        if 'type' in args:
            query = query.filter(Organisation.type == args['type'])

        return query


class OrganisationDetailView(RetrieveModelView):
    serializer_class = OrganisationSerializer
    model_class = Organisation
