from flask import request
from radar_api.serializers.organisations import OrganisationSerializer, OrganisationRequestSerializer
from radar.views.core import ListModelView, RetrieveModelView
from radar.models import Organisation


class OrganisationListView(ListModelView):
    serializer_class = OrganisationSerializer
    model_class = Organisation

    def filter_query(self, query):
        query = super(OrganisationListView, self).filter_query(query)

        serializer = OrganisationRequestSerializer()
        args = serializer.args_to_value(request.args)

        if 'type' in args:
            query = query.filter(Organisation.type == args['type'])

        if 'recruitment' in args:
            query = query.filter(Organisation.recruitment == args['recruitment'])

        return query


class OrganisationDetailView(RetrieveModelView):
    serializer_class = OrganisationSerializer
    model_class = Organisation


def register_views(app):
    app.add_url_rule('/organisations', view_func=OrganisationListView.as_view('organisation_list'))
    app.add_url_rule('/organisations/<int:id>', view_func=OrganisationDetailView.as_view('organisation_detail'))
