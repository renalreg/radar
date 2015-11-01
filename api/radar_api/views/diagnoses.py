from flask import request
from radar_api.serializers.diagnoses import CohortDiagnosisSerializer, DiagnosisSerializer, \
    CohortDiagnosisRequestSerializer
from radar.models import CohortDiagnosis, Diagnosis, DIAGNOSIS_BIOPSY_DIAGNOSES, DIAGNOSIS_KARYOTYPES
from radar.validation.diagnoses import DiagnosisValidation
from radar.views.codes import CodedIntegerListView
from radar.views.cohorts import CohortObjectViewMixin
from radar.views.core import ListModelView
from radar.views.patients import PatientObjectDetailView, PatientObjectListView


class DiagnosisListView(CohortObjectViewMixin, PatientObjectListView):
    serializer_class = DiagnosisSerializer
    validation_class = DiagnosisValidation
    model_class = Diagnosis


class DiagnosisDetailView(CohortObjectViewMixin, PatientObjectDetailView):
    serializer_class = DiagnosisSerializer
    validation_class = DiagnosisValidation
    model_class = Diagnosis


class CohortDiagnosisListView(ListModelView):
    serializer_class = CohortDiagnosisSerializer
    model_class = CohortDiagnosis

    def filter_query(self, query):
        query = super(CohortDiagnosisListView, self).filter_query(query)

        serializer = CohortDiagnosisRequestSerializer()
        args = serializer.args_to_value(request.args)

        cohort_id = args.get('cohort')

        if cohort_id is not None:
            query = query.filter(CohortDiagnosis.cohort_id == cohort_id)

        return query


class DiagnosisBiopsyDiagnosesListView(CodedIntegerListView):
    items = DIAGNOSIS_BIOPSY_DIAGNOSES


class DiagnosisKaryotypeListView(CodedIntegerListView):
    items = DIAGNOSIS_KARYOTYPES


def register_views(app):
    app.add_url_rule('/diagnoses', view_func=DiagnosisListView.as_view('diagnosis_list'))
    app.add_url_rule('/diagnoses/<id>', view_func=DiagnosisDetailView.as_view('diagnosis_detail'))
    app.add_url_rule('/diagnosis-cohort-diagnoses', view_func=CohortDiagnosisListView.as_view('diagnosis_cohort_diagnosis_list'))
    app.add_url_rule('/diagnosis-biopsy-diagnoses', view_func=DiagnosisBiopsyDiagnosesListView.as_view('diagnosis_biopsy_diagnosis_list'))
    app.add_url_rule('/diagnosis-karyotypes', view_func=DiagnosisKaryotypeListView.as_view('diagnosis_karyotype_list'))
