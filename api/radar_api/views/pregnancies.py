from radar_api.serializers.pregnancies import PregnancySerializer
from radar.models import Pregnancy, OUTCOMES, DELIVERY_METHODS, PRE_ECLAMPSIA_TYPES
from radar.validation.pregnancies import PregnancyValidation
from radar.views.codes import CodedStringListView
from radar.views.sources import DataSourceObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView


class PregnancyListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = PregnancySerializer
    model_class = Pregnancy
    validation_class = PregnancyValidation


class PregnancyDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = PregnancySerializer
    model_class = Pregnancy
    validation_class = PregnancyValidation


class PregnancyOutcomeListView(CodedStringListView):
    items = OUTCOMES


class PregnancyDeliveryMethodListView(CodedStringListView):
    items = DELIVERY_METHODS


class PregnancyPreEclampsiaTypeListView(CodedStringListView):
    items = PRE_ECLAMPSIA_TYPES


def register_views(app):
    app.add_url_rule('/pregnancies', view_func=PregnancyListView.as_view('pregnancy_list'))
    app.add_url_rule('/pregnancies/<id>', view_func=PregnancyDetailView.as_view('pregnancy_detail'))
    app.add_url_rule('/pregnancy-outcomes', view_func=PregnancyOutcomeListView.as_view('pregnancy_outcome_list'))
    app.add_url_rule('/pregnancy-delivery-methods', view_func=PregnancyDeliveryMethodListView.as_view('pregnancy_delivery_method_list'))
    app.add_url_rule('/pregnancy-pre-eclampsia-types', view_func=PregnancyPreEclampsiaTypeListView.as_view('pregnancy_pre_eclampsia_type_list'))
