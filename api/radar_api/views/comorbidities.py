from radar_api.serializers.comorbidities import ComorbiditySerializer, DisorderSerializer
from radar.validation.comorbidities import ComorbidityValidation
from radar.views.core import ListModelView
from radar.models import Comorbidity, Disorder
from radar.views.sources import SourceGroupObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView


class ComorbidityListView(SourceGroupObjectViewMixin, PatientObjectListView):
    serializer_class = ComorbiditySerializer
    validation_class = ComorbidityValidation
    model_class = Comorbidity


class ComorbidityDetailView(SourceGroupObjectViewMixin, PatientObjectDetailView):
    serializer_class = ComorbiditySerializer
    validation_class = ComorbidityValidation
    model_class = Comorbidity


class DisorderListView(ListModelView):
    serializer_class = DisorderSerializer
    model_class = Disorder

    def sort_query(self, query):
        return query.order_by(Disorder.name)


def register_views(app):
    app.add_url_rule('/comorbidities', view_func=ComorbidityListView.as_view('comorbidity_list'))
    app.add_url_rule('/comorbidities/<id>', view_func=ComorbidityDetailView.as_view('comorbidity_detail'))
    app.add_url_rule('/comorbidity-disorders', view_func=DisorderListView.as_view('disorder_list'))
