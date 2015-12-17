from flask import request

from radar_api.serializers.consultants import ConsultantSerializer, ConsultantRequestSerializer
from radar.views.core import ListModelView, RetrieveModelView, UpdateModelView, DestroyModelView, CreateModelView
from radar.models import Consultant
from radar.permissions import AdminPermission
from radar.validation.consultants import ConsultantValidation


class ConsultantListView(ListModelView):
    serializer_class = ConsultantSerializer
    model_class = Consultant
    validation_class = ConsultantValidation

    def filter_query(self, query):
        query = super(ConsultantListView, self).filter_query(query)

        serializer = ConsultantRequestSerializer()
        args = serializer.args_to_value(request.args)

        if 'patient' in args:
            pass

        return query


class ConsultantCreateView(CreateModelView):
    serializer_class = ConsultantSerializer
    model_class = Consultant
    validation_class = ConsultantValidation


class ConsultantRetrieveView(RetrieveModelView):
    serializer_class = ConsultantSerializer
    model_class = Consultant


class ConsultantUpdateView(UpdateModelView):
    serializer_class = ConsultantSerializer
    model_class = Consultant
    validation_class = ConsultantValidation
    permissions = [AdminPermission]


class ConsultantDestroyView(DestroyModelView):
    serializer_class = ConsultantSerializer
    model_class = Consultant
    permissions = [AdminPermission]


def register_views(app):
    app.add_url_rule('/consultants', view_func=ConsultantListView.as_view('consultant_list'))
    app.add_url_rule('/consultants', view_func=ConsultantCreateView.as_view('consultant_create'))
    app.add_url_rule('/consultants/<id>', view_func=ConsultantRetrieveView.as_view('consultant_retrieve'))
    app.add_url_rule('/consultants/<id>', view_func=ConsultantUpdateView.as_view('consultant_update'))
    app.add_url_rule('/consultants/<id>', view_func=ConsultantDestroyView.as_view('consultant_destroy'))
