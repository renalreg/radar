from radar.models.pregnancies import Pregnancy, OUTCOMES, DELIVERY_METHODS, PRE_ECLAMPSIA_TYPES
from radar.api.serializers.pregnancies import PregnancySerializer
from radar.api.views.common import (
    StringLookupListView,
    SourceObjectViewMixin,
    PatientObjectDetailView,
    PatientObjectListView
)


class PregnancyListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = PregnancySerializer
    model_class = Pregnancy


class PregnancyDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = PregnancySerializer
    model_class = Pregnancy


class PregnancyOutcomeListView(StringLookupListView):
    items = OUTCOMES


class PregnancyDeliveryMethodListView(StringLookupListView):
    items = DELIVERY_METHODS


class PregnancyPreEclampsiaTypeListView(StringLookupListView):
    items = PRE_ECLAMPSIA_TYPES


def register_views(app):
    app.add_url_rule('/pregnancies', view_func=PregnancyListView.as_view('pregnancy_list'))
    app.add_url_rule('/pregnancies/<id>', view_func=PregnancyDetailView.as_view('pregnancy_detail'))
    app.add_url_rule('/pregnancy-outcomes', view_func=PregnancyOutcomeListView.as_view('pregnancy_outcome_list'))
    app.add_url_rule('/pregnancy-delivery-methods', view_func=PregnancyDeliveryMethodListView.as_view('pregnancy_delivery_method_list'))
    app.add_url_rule('/pregnancy-pre-eclampsia-types', view_func=PregnancyPreEclampsiaTypeListView.as_view('pregnancy_pre_eclampsia_type_list'))
