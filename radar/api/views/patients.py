import csv
import re
import io

from backports import csv
from cornflake import fields, serializers
from cornflake.validators import none_if_blank
from flask import Response, session

from radar.auth.sessions import current_user
from radar.api.logs import log_view_patient
from radar.api.permissions import PatientPermission, AdminPermission
from radar.api.serializers.common import GroupField
from radar.api.serializers.patients import PatientSerializer, TinyPatientSerializer
from radar.api.views.generics import (
    ApiView,
    ListModelView,
    RetrieveUpdateModelView,
    DestroyModelView,
    parse_args,
    get_sort_args
)
from radar.models.patients import Patient
from radar.models.groups import Group, GROUP_TYPE
from radar.patient_search import PatientQueryBuilder
from radar.utils import uniq, get_path


class PatientListRequestSerializer(serializers.Serializer):
    id = fields.IntegerField(required=False)
    first_name = fields.StringField(required=False, validators=[none_if_blank()])
    last_name = fields.StringField(required=False, validators=[none_if_blank()])
    date_of_birth = fields.DateField(required=False)
    year_of_birth = fields.IntegerField(required=False)
    date_of_death = fields.DateField(required=False)
    year_of_death = fields.IntegerField(required=False)
    gender = fields.StringField(required=False)
    patient_number = fields.StringField(required=False, validators=[none_if_blank()])
    group = fields.CommaSeparatedField(required=False, child=GroupField())
    current = fields.BooleanField(required=False)
    ukrdc = fields.BooleanField(required=False)


def list_patients():
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
    ukrdc = args['ukrdc']

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

    if ukrdc is not None:
        builder.ukrdc(ukrdc)

    for group in groups:
        builder.group(group, current=current)

    sort, reverse = get_sort_args()

    if sort is not None:
        m = re.match('^group_([0-9]+)', sort)

        if m:
            group = Group.query.get(int(m.group(1)))

            if group is not None:
                builder.sort_by_group(group, reverse)
        else:
            builder.sort(sort, reverse)

    query = builder.build(current=current)

    return query


class PatientListView(ListModelView):
    serializer_class = TinyPatientSerializer
    model_class = Patient
    permission_classes = [PatientPermission]

    def get_query(self):
        return list_patients()

    def get_object_list(self):
        patients, pagination = super(PatientListView, self).get_object_list()
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


class PatientListCSVView(ApiView):
    def get(self):
        f = io.StringIO()
        writer = csv.writer(f)

        headers = [
            'Patient ID',
            'First Name', 'Last Name',
            'Gender',
            'Date of Birth', 'Year of Birth', 'Date of Death', 'Year of Death',
            'Patient Number',
            'Recruited On', 'Recruited Group',
            'Cohorts', 'Hospitals',
        ]
        writer.writerow(headers)

        def get_groups(data, group_type):
            group_type = group_type.value
            groups = [x['group']['name'] for x in data['groups'] if x['group']['type'] == group_type]
            groups = sorted(groups)
            groups = uniq(groups)
            return ', '.join(groups)

        patients = list_patients()

        for patient in patients:
            data = TinyPatientSerializer(instance=patient, context={'user': current_user}).data

            output = []
            output.append(get_path(data, 'id'))
            output.append(get_path(data, 'first_name'))
            output.append(get_path(data, 'last_name'))
            output.append(get_path(data, 'gender', 'label'))
            output.append(get_path(data, 'date_of_birth'))
            output.append(get_path(data, 'year_of_birth'))
            output.append(get_path(data, 'date_of_death'))
            output.append(get_path(data, 'year_of_death'))
            output.append(get_path(data, 'primary_patient_number', 'number'))
            output.append(get_path(data, 'recruited_date'))
            output.append(get_path(data, 'recruited_group', 'name'))
            output.append(get_groups(data, GROUP_TYPE.COHORT))
            output.append(get_groups(data, GROUP_TYPE.HOSPITAL))

            writer.writerow(output)

        return Response(f.getvalue(), content_type='text/csv')


def register_views(app):
    app.add_url_rule('/patients', view_func=PatientListView.as_view('patient_list'))
    app.add_url_rule('/patients/<int:id>', view_func=PatientDetailView.as_view('patient_detail'))
    app.add_url_rule('/patients/<int:id>', view_func=PatientDestroyView.as_view('patient_destroy'))
    app.add_url_rule('/patients.csv', view_func=PatientListCSVView.as_view('patient_list_csv'))
