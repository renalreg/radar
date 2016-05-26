from radar.api.serializers.pkd import LiverImagingSerializer, LiverSymptomsSerializer, LiverTransplantSerializer
from radar.api.views.common import (
    StringLookupListView,
    SourceObjectViewMixin,
    PatientObjectDetailView,
    PatientObjectListView
)
from radar.models.pkd import (
    LiverImaging,
    LIVER_IMAGING_TYPES,
    LiverSymptoms,
    LiverTransplant,
    INDICATIONS,
    FIRST_GRAFT_SOURCES,
    LOSS_REASONS
)


class LiverImagingListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = LiverImagingSerializer
    model_class = LiverImaging


class LiverImagingDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = LiverImagingSerializer
    model_class = LiverImaging


class LiverImagingTypeListView(StringLookupListView):
    items = LIVER_IMAGING_TYPES


class LiverSymptomsListView(PatientObjectListView):
    serializer_class = LiverSymptomsSerializer
    model_class = LiverSymptoms


class LiverSymptomsDetailView(PatientObjectDetailView):
    serializer_class = LiverSymptomsSerializer
    model_class = LiverSymptoms


class LiverTransplantListView(PatientObjectListView):
    serializer_class = LiverTransplantSerializer
    model_class = LiverTransplant


class LiverTransplantDetailView(PatientObjectDetailView):
    serializer_class = LiverTransplantSerializer
    model_class = LiverTransplant


class LiverTransplantIndicationListView(StringLookupListView):
    items = INDICATIONS


class LiverTransplantFirstGraftSourceListView(StringLookupListView):
    items = FIRST_GRAFT_SOURCES


class LiverTransplantLossReasonListView(StringLookupListView):
    items = LOSS_REASONS


def register_views(app):
    app.add_url_rule('/liver-imaging', view_func=LiverImagingListView.as_view('liver_imaging_list'))
    app.add_url_rule('/liver-imaging/<id>', view_func=LiverImagingDetailView.as_view('liver_imaging_detail'))
    app.add_url_rule('/liver-imaging-types', view_func=LiverImagingTypeListView.as_view('liver_imaging_type_list'))

    app.add_url_rule('/liver-symptoms', view_func=LiverSymptomsListView.as_view('liver_symptoms_list'))
    app.add_url_rule('/liver-symptoms/<id>', view_func=LiverSymptomsDetailView.as_view('liver_symptoms_detail'))

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
