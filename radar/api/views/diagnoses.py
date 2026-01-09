from collections import OrderedDict

from cornflake import fields, serializers
from flask import request
from sqlalchemy.orm import subqueryload

from radar.api.permissions import AdminPermission
from radar.api.serializers.common import QueryPatientField
from radar.api.serializers.diagnoses import (
    DiagnosisSerializer,
    PatientDiagnosisSerializer,
)
from radar.api.views.common import (
    IntegerLookupListView,
    PatientObjectDetailView,
    PatientObjectListView,
    SourceObjectViewMixin,
    StringLookupListView
)
from radar.api.views.generics import (
    CreateModelView,
    DestroyModelView,
    ListModelView,
    parse_args,
    RetrieveModelView,
    UpdateModelView, response_json, ApiView,
)
from radar.database import db
from radar.models import GroupAntibody, Antibody
from radar.models.diagnoses import (
    BIOPSY_DIAGNOSES,
    Diagnosis,
    GROUP_DIAGNOSIS_TYPE,
    GROUP_DIAGNOSIS_TYPE_NAMES,
    GroupDiagnosis,
    PatientDiagnosis
)
from radar.models.groups import Group


class DiagnosisRequestSerializer(serializers.Serializer):
    primary_group = fields.CommaSeparatedField(child=fields.IntegerField(), required=False)
    secondary_group = fields.CommaSeparatedField(child=fields.IntegerField(), required=False)


class PatientDiagnosisRequestSerializer(serializers.Serializer):
    primary_group = fields.CommaSeparatedField(child=fields.IntegerField(), required=False)
    secondary_group = fields.CommaSeparatedField(child=fields.IntegerField(), required=False)
    include_primary = fields.BooleanField(default=True)
    include_secondary = fields.BooleanField(default=True)
    patient = QueryPatientField(required=False)


def patient_diagnosis_group_type_filter(group_ids, group_diagnosis_type):
    return _diagnosis_group_type_filter(PatientDiagnosis.diagnosis_id, group_ids, group_diagnosis_type)


def diagnosis_group_type_filter(group_ids, group_diagnosis_type):
    return _diagnosis_group_type_filter(Diagnosis.id, group_ids, group_diagnosis_type)


def _diagnosis_group_type_filter(diagnois_column, group_ids, group_diagnosis_type):
    return GroupDiagnosis.query\
        .filter(GroupDiagnosis.group_id.in_(group_ids))\
        .filter(GroupDiagnosis.diagnosis_id == diagnois_column)\
        .filter(GroupDiagnosis.type == group_diagnosis_type)\
        .exists()


class PatientDiagnosisListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = PatientDiagnosisSerializer
    model_class = PatientDiagnosis

    def filter_query(self, query):
        query = super(PatientDiagnosisListView, self).filter_query(query)

        args = parse_args(PatientDiagnosisRequestSerializer)

        primary_group_ids = args['primary_group']
        secondary_group_ids = args['secondary_group']
        include_primary = args['include_primary']
        include_secondary = args['include_secondary']
        patient = args['patient']

        # Primary diagnosis for any of these groups
        if primary_group_ids:
            query = query.filter(patient_diagnosis_group_type_filter(primary_group_ids, GROUP_DIAGNOSIS_TYPE.PRIMARY))

        # Secondary diagnosis for any of these groups
        if secondary_group_ids:
            query = query.filter(
                patient_diagnosis_group_type_filter(
                    secondary_group_ids,
                    GROUP_DIAGNOSIS_TYPE.SECONDARY
                )
            )

        # Excluding primary or secondary diagnoses
        if not include_primary or not include_secondary:
            # Only exclude diagnoses that are primary/secondary for this patient
            if patient:
                groups = patient.groups
            else:
                groups = Group.query.all()

            group_ids = [x.id for x in groups]

            if not include_primary:
                # Exclude primary diagnoses
                query = query.filter(~patient_diagnosis_group_type_filter(group_ids, GROUP_DIAGNOSIS_TYPE.PRIMARY))

            if not include_secondary:
                # Exclude secondary diagnoses
                query = query.filter(~patient_diagnosis_group_type_filter(group_ids, GROUP_DIAGNOSIS_TYPE.SECONDARY))

        return query


class PatientDiagnosisDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = PatientDiagnosisSerializer
    model_class = PatientDiagnosis


class DiagnosisListView(ListModelView):
    serializer_class = DiagnosisSerializer
    model_class = Diagnosis

    def filter_query(self, query):
        query = super(DiagnosisListView, self).filter_query(query)

        # Load codes and groups in subqueries rather than lazy-loading (to avoid O(n) queries)
        query = query.options(subqueryload('diagnosis_codes').joinedload('code'))
        query = query.options(subqueryload('group_diagnoses').joinedload('group'))

        args = parse_args(DiagnosisRequestSerializer)

        primary_group_ids = args['primary_group']
        secondary_group_ids = args['secondary_group']

        if primary_group_ids:
            query = query.filter(diagnosis_group_type_filter(primary_group_ids, GROUP_DIAGNOSIS_TYPE.PRIMARY))

        if secondary_group_ids:
            query = query.filter(diagnosis_group_type_filter(secondary_group_ids, GROUP_DIAGNOSIS_TYPE.SECONDARY))

        return query


class DiagnosisCreateView(CreateModelView):
    serializer_class = DiagnosisSerializer
    model_class = Diagnosis
    permissions = [AdminPermission]


class DiagnosisRetrieveView(RetrieveModelView):
    serializer_class = DiagnosisSerializer
    model_class = Diagnosis


class DiagnosisUpdateView(UpdateModelView):
    serializer_class = DiagnosisSerializer
    model_class = Diagnosis
    permissions = [AdminPermission]


class DiagnosisDestroyView(DestroyModelView):
    model_class = Diagnosis
    permissions = [AdminPermission]


class BiopsyDiagnosisListView(IntegerLookupListView):
    items = BIOPSY_DIAGNOSES


class GroupDiagnosisTypeListView(StringLookupListView):
    items = GROUP_DIAGNOSIS_TYPE_NAMES






# Request serializer for input validation
class GroupAntibodiesRequestSerializer(serializers.Serializer):
    group_id = fields.IntegerField(required=True)


class AntibodyListView(StringLookupListView):
    permissions = [AdminPermission]
    @property
    def items(self):
        # Build the base query
        query = self.filter_query(Antibody.query)

        # Return as OrderedDict {id: id} for StringLookupListView
        return OrderedDict((a.id, a.id) for a in query.all())

    def filter_query(self, query):
        """
        Filter antibodies based on cohort_id query parameter.
        Only include official antibodies mapped to the cohort's group.
        """

        # Get cohort_id from query params
        cohort_code = request.args.get('group_id')
        if not cohort_code:
            return query.filter(False)  # No cohort -> return empty query

        # Filter: official antibodies linked to this group
        query = (
            query.join(Antibody.group_antibodies)
                 .filter(GroupAntibody.group_id == cohort_code)
                 .filter(Antibody.is_official==True)
                 .order_by(Antibody.id)
        )
        return query


def register_views(app):
    app.add_url_rule('/patient-diagnoses', view_func=PatientDiagnosisListView.as_view('patient_diagnosis_list'))
    app.add_url_rule(
        '/patient-diagnoses/<id>',
        view_func=PatientDiagnosisDetailView.as_view('patient_diagnosis_detail'))
    app.add_url_rule('/diagnoses', view_func=DiagnosisListView.as_view('diagnosis_list'))
    app.add_url_rule('/diagnoses', view_func=DiagnosisCreateView.as_view('diagnosis_create'))
    app.add_url_rule('/diagnoses/<id>', view_func=DiagnosisRetrieveView.as_view('diagnosis_retrieve'))
    app.add_url_rule('/diagnoses/<id>', view_func=DiagnosisUpdateView.as_view('diagnosis_update'))
    app.add_url_rule('/diagnoses/<id>', view_func=DiagnosisDestroyView.as_view('diagnosis_destroy'))
    app.add_url_rule('/biopsy-diagnoses', view_func=BiopsyDiagnosisListView.as_view('biopsy_diagnosis_list'))
    app.add_url_rule(
        '/group-diagnosis-types',
        view_func=GroupDiagnosisTypeListView.as_view('group_diagnosis_type_list')
    )
    app.add_url_rule('/antibodies',view_func=AntibodyListView.as_view('group_antibodies'))


