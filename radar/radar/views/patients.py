from cornflake import fields, serializers
from cornflake.validators import none_if_empty

from radar.patient_search import PatientQueryBuilder
from radar.logs import log_view_patients, log_view_patient
from radar.auth.sessions import current_user
from radar.models.patients import Patient
from radar.serializers.patients import PatientSerializer, TinyPatientSerializer
from radar.serializers.common import GroupField
from radar.permissions import PatientPermission, AdminPermission
from radar.views.generics import (
    ListModelView,
    RetrieveUpdateModelView,
    DestroyModelView,
    parse_args
)


class PatientListRequestSerializer(serializers.Serializer):
    id = fields.IntegerField(required=False)
    first_name = fields.StringField(required=False, validators=[none_if_empty()])
    last_name = fields.StringField(required=False, validators=[none_if_empty()])
    date_of_birth = fields.DateField(required=False)
    year_of_birth = fields.IntegerField(required=False)
    date_of_death = fields.DateField(required=False)
    year_of_death = fields.IntegerField(required=False)
    gender = fields.StringField(required=False)
    patient_number = fields.StringField(required=False, validators=[none_if_empty()])
    group = fields.CommaSeparatedField(required=False, child=GroupField())
    current = fields.BooleanField(required=False)


class PatientListView(ListModelView):
    serializer_class = TinyPatientSerializer
    model_class = Patient
    permission_classes = [PatientPermission]

    def get_query(self):
        args = parse_args(PatientListRequestSerializer)

        builder = PatientQueryBuilder(current_user)

        patient_id = args['id']
        first_name = args['first_name']
        last_name = args['last_name']
        patient_number = args['patient_number']
        gender = args['gender']
        date_of_birth = args['date_of_birth']
        year_of_birth = args['year_of_birth']
        date_of_death = args['date_of_death']
        year_of_death = args['year_of_death']
        groups = args['group']
        current = args['current']

        if patient_id is not None:
            builder.patient_id(patient_id)

        if first_name is not None:
            builder.first_name(first_name)

        if last_name is not None:
            builder.last_name(last_name)

        if patient_number is not None:
            builder.patient_number(patient_number)

        if gender is not None:
            builder.gender(gender)

        if date_of_birth is not None:
            builder.date_of_birth(date_of_birth)

        if year_of_birth is not None:
            builder.year_of_birth(year_of_birth)

        if date_of_death is not None:
            builder.date_of_death(date_of_death)

        if year_of_death is not None:
            builder.year_of_death(year_of_death)

        for group in groups:
            builder.group(group, current=current)

        sort, reverse = self.get_sort_args()

        if sort is not None:
            builder.sort(sort, reverse)

        query = builder.build(current=current)

        return query

    def get_object_list(self):
        patients, pagination = super(PatientListView, self).get_object_list()
        log_view_patients(patients)
        return patients, pagination


class PatientDetailView(RetrieveUpdateModelView):
    serializer_class = PatientSerializer
    model_class = Patient
    permission_classes = [PatientPermission]

    def get_query(self):
        builder = PatientQueryBuilder(current_user)
        return builder.build()

    def get_object(self):
        patient = super(PatientDetailView, self).get_object()
        log_view_patient(patient)
        return patient


class PatientDestroyView(DestroyModelView):
    model_class = Patient
    permission_classes = [AdminPermission]


def register_views(app):
    app.add_url_rule('/patients', view_func=PatientListView.as_view('patient_list'))
    app.add_url_rule('/patients/<int:id>', view_func=PatientDetailView.as_view('patient_detail'))
    app.add_url_rule('/patients/<int:id>', view_func=PatientDestroyView.as_view('patient_destroy'))
