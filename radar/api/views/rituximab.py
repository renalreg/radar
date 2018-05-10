from radar.api.serializers.rituximab import RituximabBaselineAssessmentSerializer
from radar.api.views.common import (
    IntegerLookupListView,
    PatientObjectDetailView,
    PatientObjectListView,
    StringLookupListView,
)
from radar.models.rituximab import (
    BaselineAssessment,
    PERFORMANCE_STATUS_OPTIONS,
    TREATMENT_OPTIONS,
)


class RituximabBaselineAssessmentListView(PatientObjectListView):
    serializer_class = RituximabBaselineAssessmentSerializer
    model_class = BaselineAssessment


class RituximabBaselineAssessmentDetailView(PatientObjectDetailView):
    serializer_class = RituximabBaselineAssessmentSerializer
    model_class = BaselineAssessment


class RituximabTreatmentOptionListView(StringLookupListView):
    items = TREATMENT_OPTIONS


class RituximabPerformanceOptionListView(IntegerLookupListView):
    items = PERFORMANCE_STATUS_OPTIONS


def register_views(app):
    app.add_url_rule(
        '/rituximab-baseline-assessment',
        view_func=RituximabBaselineAssessmentListView.as_view('rituximab_baseline_assessment')
    )
    app.add_url_rule(
        '/rituximab-treatment-options',
        view_func=RituximabTreatmentOptionListView.as_view('rituximab_treatment_option_list'))

    app.add_url_rule(
        '/rituximab-performance-options',
        view_func=RituximabPerformanceOptionListView.as_view('rituximab_performance_option_list'))

    app.add_url_rule(
        '/rituximab-baseline-assessment/<id>',
        view_func=RituximabBaselineAssessmentDetailView.as_view('assessment_detail')
    )
