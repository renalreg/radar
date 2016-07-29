from radar.api.serializers.pkd import (
    LiverImagingSerializer,
    LiverDiseasesSerializer,
    LiverTransplantSerializer,
    NutritionSerializer
)
from radar.api.views.common import (
    StringLookupListView,
    SourceObjectViewMixin,
    PatientObjectDetailView,
    PatientObjectListView
)
from radar.models.pkd import (
    LiverImaging,
    LIVER_IMAGING_TYPES,
    LiverDiseases,
    LiverTransplant,
    INDICATIONS,
    FIRST_GRAFT_SOURCES,
    LOSS_REASONS,
    Nutrition,
    FEEDING_TYPES
)


class LiverImagingListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = LiverImagingSerializer
    model_class = LiverImaging


class LiverImagingDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = LiverImagingSerializer
    model_class = LiverImaging


class LiverImagingTypeListView(StringLookupListView):
    items = LIVER_IMAGING_TYPES


class LiverDiseasesListView(PatientObjectListView):
    serializer_class = LiverDiseasesSerializer
    model_class = LiverDiseases


class LiverDiseasesDetailView(PatientObjectDetailView):
    serializer_class = LiverDiseasesSerializer
    model_class = LiverDiseases


class LiverTransplantListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = LiverTransplantSerializer
    model_class = LiverTransplant


class LiverTransplantDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = LiverTransplantSerializer
    model_class = LiverTransplant


class LiverTransplantIndicationListView(StringLookupListView):
    items = INDICATIONS


class LiverTransplantFirstGraftSourceListView(StringLookupListView):
    items = FIRST_GRAFT_SOURCES


# TODO rename to failure reason?
class LiverTransplantLossReasonListView(StringLookupListView):
    items = LOSS_REASONS


class NutritionListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = NutritionSerializer
    model_class = Nutrition


class NutritionDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = NutritionSerializer
    model_class = Nutrition


class NutritionFeedingTypeListView(StringLookupListView):
    items = FEEDING_TYPES


def register_views(app):
    app.add_url_rule('/liver-imaging', view_func=LiverImagingListView.as_view('liver_imaging_list'))
    app.add_url_rule('/liver-imaging/<id>', view_func=LiverImagingDetailView.as_view('liver_imaging_detail'))
    app.add_url_rule('/liver-imaging-types', view_func=LiverImagingTypeListView.as_view('liver_imaging_type_list'))

    app.add_url_rule('/liver-diseases', view_func=LiverDiseasesListView.as_view('liver_diseases_list'))
    app.add_url_rule('/liver-diseases/<id>', view_func=LiverDiseasesDetailView.as_view('liver_diseases_detail'))

    app.add_url_rule('/liver-transplants', view_func=LiverTransplantListView.as_view('liver_transplant_list'))
    app.add_url_rule('/liver-transplants/<id>', view_func=LiverTransplantDetailView.as_view('liver_transplant_detail'))
    app.add_url_rule(
        '/liver-transplant-indications',
        view_func=LiverTransplantIndicationListView.as_view('liver_transplant_indication_list')
    )
    app.add_url_rule(
        '/liver-transplant-first-graft-sources',
        view_func=LiverTransplantFirstGraftSourceListView.as_view('liver_transplant_first_graft_source_list')
    )
    app.add_url_rule(
        '/liver-transplant-loss-reasons',
        view_func=LiverTransplantLossReasonListView.as_view('liver_transplant_loss_reason_list')
    )

    app.add_url_rule('/nutrition', view_func=NutritionListView.as_view('nutrition_list'))
    app.add_url_rule('/nutrition/<id>', view_func=NutritionDetailView.as_view('nutrition_detail'))
    app.add_url_rule('/nutrition-feeding-types', view_func=NutritionFeedingTypeListView.as_view('nutrition_feeding_type_list'))
