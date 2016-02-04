from radar_api.serializers.renal_progressions import RenalProgressionSerializer
from radar.models.renal_progressions import RenalProgression
from radar.validation.renal_progressions import RenalProgressionValidation
from radar.views.patients import PatientObjectDetailView, PatientObjectListView


class RenalProgressionListView(PatientObjectListView):
    serializer_class = RenalProgressionSerializer
    model_class = RenalProgression
    validation_class = RenalProgressionValidation


class RenalProgressionDetailView(PatientObjectDetailView):
    serializer_class = RenalProgressionSerializer
    model_class = RenalProgression
    validation_class = RenalProgressionValidation


def register_views(app):
    app.add_url_rule('/renal-progressions', view_func=RenalProgressionListView.as_view('renal_progression_list'))
    app.add_url_rule('/renal-progressions/<id>', view_func=RenalProgressionDetailView.as_view('renal_progression_detail'))
