from radar.api.serializers.nurture_tubes import OptionSerializer, SamplesSerializer
from radar.api.views.common import (
    PatientObjectDetailView,
    PatientObjectListView,
    StringLookupListView,
)
from radar.api.views.generics import ListModelView

from radar.models.nurture_tubes import SampleOption, Samples


class SamplesListView(PatientObjectListView):
    serializer_class = SamplesSerializer
    model_class = Samples


class SamplesDetailView(PatientObjectDetailView):
    serializer_class = SamplesSerializer
    model_class = Samples


#class SamplesProtocolOptions(StringLookupListView):
#    items = PROTOCOL_OPTIONS


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


