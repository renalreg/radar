from radar.models.plasmapheresis import Plasmapheresis, PLASMAPHERESIS_RESPONSES, PLASMAPHERESIS_NO_OF_EXCHANGES
from radar.serializers.plasmapheresis import PlasmapheresisSerializer
from radar.views.common import (
    PatientObjectListView,
    PatientObjectDetailView,
    StringLookupListView,
    SourceObjectViewMixin
)


class PlasmapheresisListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = PlasmapheresisSerializer
    model_class = Plasmapheresis


class PlasmapheresisDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = PlasmapheresisSerializer
    model_class = Plasmapheresis


class PlasmapheresisResponseListView(StringLookupListView):
    items = PLASMAPHERESIS_RESPONSES


class PlasmapheresisNoOfExchangesListView(StringLookupListView):
    items = PLASMAPHERESIS_NO_OF_EXCHANGES


def register_views(app):
    app.add_url_rule('/plasmapheresis', view_func=PlasmapheresisListView.as_view('plasmapheresis_list'))
    app.add_url_rule('/plasmapheresis/<id>', view_func=PlasmapheresisDetailView.as_view('plasmapheresis_detail'))
    app.add_url_rule('/plasmapheresis-responses', view_func=PlasmapheresisResponseListView.as_view('plasmapheresis_response_list'))
    app.add_url_rule('/plasmapheresis-no-of-exchanges', view_func=PlasmapheresisNoOfExchangesListView.as_view('plasmapheresis_no_of_exchanges_list'))
