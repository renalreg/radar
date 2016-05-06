from radar.models.renal_progressions import RenalProgression
from radar.serializers.renal_progressions import RenalProgressionSerializer
from radar.views.common import PatientObjectDetailView, PatientObjectListView


class RenalProgressionListView(PatientObjectListView):
    serializer_class = RenalProgressionSerializer
    model_class = RenalProgression


class RenalProgressionDetailView(PatientObjectDetailView):
    serializer_class = RenalProgressionSerializer
    model_class = RenalProgression


def register_views(app):
    app.add_url_rule('/renal-progressions', view_func=RenalProgressionListView.as_view('renal_progression_list'))
    app.add_url_rule('/renal-progressions/<id>', view_func=RenalProgressionDetailView.as_view('renal_progression_detail'))
