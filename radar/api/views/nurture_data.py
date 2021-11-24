from radar.api.serializers.nurture_data import NurtureDataSerializer
from radar.api.views.common import (
    PatientObjectDetailView,
    PatientObjectListView,
    StringLookupListView,
)
from radar.models.nurture_data import SIGNED_OFF, NurtureData


class NurtureDataListView(PatientObjectListView):
    serializer_class = NurtureDataSerializer
    model_class = NurtureData


class NurtureDataDetailView(PatientObjectDetailView):
    serializer_class = NurtureDataSerializer
    model_class = NurtureData


class SignedOfStatesListView(StringLookupListView):
    items = SIGNED_OFF


def register_views(app):
    app.add_url_rule(
        "/nurture-data", view_func=NurtureDataListView.as_view("nurture_data_list")
    )
    app.add_url_rule(
        "/nurture-data/<id>",
        view_func=NurtureDataDetailView.as_view("nurture_data_detail"),
    )
    app.add_url_rule(
        "/signed-off-states",
        view_func=SignedOfStatesListView.as_view("signed-off-states"),
    )
