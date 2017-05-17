from flask import jsonify, request

from radar.api.serializers.nurture_tubes import OptionSerializer, SamplesSerializer
from radar.api.views.common import (
    PatientObjectDetailView,
    PatientObjectListView,
)
from radar.api.views.generics import ListModelView
from radar.database import db
from radar.exceptions import BadRequest
from radar.models.nurture_tubes import PROTOCOL_OPTION_TYPE, SampleOption, Samples
from radar.utils import camel_case_keys


class SamplesListView(PatientObjectListView):
    serializer_class = SamplesSerializer
    model_class = Samples

    def create(self, *args, **kwargs):
        json = request.get_json()

        if json is None:
            raise BadRequest()

        json['protocol'] = PROTOCOL_OPTION_TYPE(json['protocol'])

        serializer = self.get_serializer(data=json)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()

        db.session.add(obj)
        db.session.commit()

        data = serializer.data
        data = camel_case_keys(data)

        return jsonify(data), 200


class SamplesDetailView(PatientObjectDetailView):
    serializer_class = SamplesSerializer
    model_class = Samples


class SamplesProtocolOptions(ListModelView):
    serializer_class = OptionSerializer
    model_class = SampleOption


def register_views(app):
    app.add_url_rule('/samples', view_func=SamplesListView.as_view('samples_list'))
    app.add_url_rule('/samples/<id>', view_func=SamplesDetailView.as_view('samples_detail'))
    app.add_url_rule(
        '/samples-protocol-options',
        view_func=SamplesProtocolOptions.as_view('samples-protocol-options')
    )
