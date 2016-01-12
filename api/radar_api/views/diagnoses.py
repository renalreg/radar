from flask import request
from radar_api.serializers.diagnoses import GroupDiagnosisSerializer, DiagnosisSerializer, \
    GroupDiagnosisRequestSerializer
from radar.models.diagnoses import GroupDiagnosis, Diagnosis, DIAGNOSIS_BIOPSY_DIAGNOSES
from radar.validation.diagnoses import DiagnosisValidation
from radar.views.codes import CodedIntegerListView
from radar.views.groups import GroupObjectViewMixin
from radar.views.core import ListModelView
from radar.views.patients import PatientObjectDetailView, PatientObjectListView


class DiagnosisListView(GroupObjectViewMixin, PatientObjectListView):
    serializer_class = DiagnosisSerializer
    validation_class = DiagnosisValidation
    model_class = Diagnosis


class DiagnosisDetailView(GroupObjectViewMixin, PatientObjectDetailView):
    serializer_class = DiagnosisSerializer
    validation_class = DiagnosisValidation
    model_class = Diagnosis


class GroupDiagnosisListView(ListModelView):
    serializer_class = GroupDiagnosisSerializer
    model_class = GroupDiagnosis

    def filter_query(self, query):
        query = super(GroupDiagnosisListView, self).filter_query(query)

        serializer = GroupDiagnosisRequestSerializer()
        args = serializer.args_to_value(request.args)

        group_id = args.get('group')

        if group_id is not None:
            query = query.filter(GroupDiagnosis.group_id == group_id)

        return query


class DiagnosisBiopsyDiagnosesListView(CodedIntegerListView):
    items = DIAGNOSIS_BIOPSY_DIAGNOSES


def register_views(app):
    app.add_url_rule('/diagnoses', view_func=DiagnosisListView.as_view('diagnosis_list'))
    app.add_url_rule('/diagnoses/<id>', view_func=DiagnosisDetailView.as_view('diagnosis_detail'))
    app.add_url_rule('/diagnosis-biopsy-diagnoses', view_func=DiagnosisBiopsyDiagnosesListView.as_view('diagnosis_biopsy_diagnosis_list'))
