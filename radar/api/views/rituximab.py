from radar.api.serializers.rituximab import (
    RituximabBaselineAssessmentSerializer,
    RituximabCriteriaSerializer,
)
from radar.api.views.common import (
    IntegerLookupListView,
    PatientObjectDetailView,
    PatientObjectListView,
    StringLookupListView,
)
from radar.models.rituximab import (
    BaselineAssessment,
    NEPHROPATHY_TYPES,
    PERFORMANCE_STATUS_OPTIONS,
    RituximabCriteria,
    SUPPORTIVE_MEDICATIONS,
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


class RituximabNephropathiesListView(StringLookupListView):
    items = NEPHROPATHY_TYPES


class SupportiveMedicationListView(StringLookupListView):
    items = SUPPORTIVE_MEDICATIONS


class RituximabCriteriaListView(PatientObjectListView):
    serializer_class = RituximabCriteriaSerializer
    model_class = RituximabCriteria


class RituximabCriteriaDetailView(PatientObjectDetailView):
    serializer_class = RituximabCriteriaSerializer
    model_class = RituximabCriteria


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

    app.add_url_rule(
        '/rituximab-nephropathies-list',
        view_func=RituximabNephropathiesListView.as_view('rituximab-nephropathies-list')
    )

    app.add_url_rule(
        '/rituximab-supportive-medication-list',
        view_func=SupportiveMedicationListView.as_view('rituximab-supportive-medication-list')
    )

    app.add_url_rule(
        '/rituximab-criteria',
        view_func=RituximabCriteriaListView.as_view('rituximab-criteria-list')
    )

    app.add_url_rule(
        '/rituximab-criteria/<id>',
        view_func=RituximabCriteriaDetailView.as_view('rituximab-criteria-detail')
    )
