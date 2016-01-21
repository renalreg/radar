from radar_api.serializers.diagnoses import DiagnosisSerializer, PatientDiagnosisSerializer
from radar.models.diagnoses import Diagnosis, PatientDiagnosis, BIOPSY_DIAGNOSES
from radar.validation.diagnoses import PatientDiagnosisValidation
from radar.views.sources import SourceObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView
from radar.views.core import ListModelView
from radar.views.codes import CodedStringListView


class PatientDiagnosisListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = PatientDiagnosisSerializer
    validation_class = PatientDiagnosisValidation
    model_class = PatientDiagnosis


class PatientDiagnosisDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = PatientDiagnosisSerializer
    validation_class = PatientDiagnosisValidation
    model_class = PatientDiagnosis


class DiagnosisListView(ListModelView):
    serializer_class = DiagnosisSerializer
    model_class = Diagnosis

    # TODO
    """
    def filter_query(self, query):
        query = super(DisorderListView, self).filter_query(query)

        serializer = DisorderRequestSerializer()
        args = serializer.args_to_value(request.args)

        group_id = args.get('group')

        if group_id is not None:
            query = query.join(Disorder.group_disorders)
            query = query.filter(GroupDisorder.group_id == group_id)

        return query
    """


class BiopsyDiagnosisListView(CodedStringListView):
    items = BIOPSY_DIAGNOSES


def register_views(app):
    app.add_url_rule('/patient-diagnoses', view_func=PatientDiagnosisListView.as_view('patient_diagnosis_list'))
    app.add_url_rule('/patient-diagnoses/<id>', view_func=PatientDiagnosisDetailView.as_view('patient_diagnosis_detail'))
    app.add_url_rule('/diagnoses', view_func=DiagnosisListView.as_view('diagnosis_list'))
    app.add_url_rule('/biopsy-diagnoses', view_func=BiopsyDiagnosisListView.as_view('biopsy_diagnosis_list'))
