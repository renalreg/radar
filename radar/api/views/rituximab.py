from radar.api.serializers.rituximab import RituximabBaselineAssessmentSerializer
from radar.api.views.common import (
    PatientObjectDetailView,
    PatientObjectListView,
)
from radar.models.rituximab import BaselineAssessment


class RituximabBaselineAssessmentListView(PatientObjectListView):
    serializer_class = RituximabBaselineAssessmentSerializer
    model_class = BaselineAssessment


class RituximabBaselineAssessmentDetailView(PatientObjectDetailView):
    serializer_class = RituximabBaselineAssessmentSerializer
    model_class = BaselineAssessment


def register_views(app):
    app.add_url_rule(
        '/rituximab-baseline-assessment',
        view_func=RituximabBaselineAssessmentListView.as_view('rituximab_baseline_assessment')
    )
