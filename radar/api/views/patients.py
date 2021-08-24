import csv
import io
import re

from cornflake import fields, serializers
from cornflake.validators import none_if_blank
from flask import Response

from radar.api.logs import log_view_patient
from radar.api.permissions import AdminPermission, PatientPermission
from radar.api.serializers.common import GroupField
from radar.api.serializers.patients import (
    PatientProxy,
    PatientSerializer,
    TinyPatientSerializer,
)
from radar.api.views.generics import (
    ApiView,
    DestroyModelView,
    get_sort_args,
    ListModelView,
    parse_args,
    RetrieveUpdateModelView,
)
from radar.auth.sessions import current_user
from radar.models.groups import Group, GROUP_TYPE
from radar.models.patients import CONSENT_STATUS, Patient
from radar.patient_search import PatientQueryBuilder
from radar.utils import get_attrs, SkipProxy, uniq


class PatientListRequestSerializer(serializers.Serializer):
    id = fields.IntegerField(required=False)
    orpha_code = fields.StringField(required=False, validators=[none_if_blank()])
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
    test = fields.BooleanField(required=False)
    control = fields.BooleanField(required=False)
    signed_off = fields.BooleanField(required=False)
    consent_status = fields.EnumField(required=False, enum=CONSENT_STATUS)


def list_patients():
    args = parse_args(PatientListRequestSerializer)

    builder = PatientQueryBuilder(current_user)

    patient_id = args["id"]
    orpha_code = args["orpha_code"]
    first_name = args["first_name"]
    last_name = args["last_name"]
    patient_number = args["patient_number"]
    gender = args["gender"]
    date_of_birth = args["date_of_birth"]
    year_of_birth = args["year_of_birth"]
    date_of_death = args["date_of_death"]
    year_of_death = args["year_of_death"]
    groups = args["group"]
    current = args["current"]
    ukrdc = args["ukrdc"]
    test = args["test"]
    control = args["control"]

    if patient_id is not None:
        builder.patient_id(patient_id)

    if orpha_code is not None:
        builder.patient_diagnosis(orpha_code)

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

    if test is not None:
        builder.test(test)

    if control is not None:
        builder.control(control)

    for group in groups:
        builder.group(group, current=current)

    sort, reverse = get_sort_args()

    if sort is not None:
        # Check if we are sorting by group recruitment date
        m = re.match("^group_([0-9]+)", sort)

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
        args = parse_args(PatientListRequestSerializer)

        cohorts = [i for i in args["group"] if i.type == GROUP_TYPE.COHORT]

        headers = [
            "Patient ID",
            "First Name",
            "Last Name",
            "Date of Birth",
            "Year of Birth",
            "Date of Death",
            "Year of Death",
            "Gender",
            "Gender Label",
            "Ethnicity",
            "Ethnicity Label",
            "Patient Number",
            "PV",
            "Recruited On",
            "Recruited Group Name",
            "Recruited Group Code",
            "Cohorts",
            "Hospitals",
        ]
        for cohort in cohorts:
            headers.append(cohort.short_name)

        writer.writerow(headers)

        def get_groups(patient, group_type):
            """Comma-separated list of groups."""

            groups = [x.name for x in patient.current_groups if x.type == group_type]
            groups = sorted(groups)
            groups = uniq(groups)
            return ", ".join(groups)

        patients = list_patients()

        for patient in patients:
            # Wrap the patient so demographics aren't exposed to unprivileged users
            patient = SkipProxy(PatientProxy(patient, current_user))

            output = []
            output.append(patient.id)
            output.append(patient.first_name)
            output.append(patient.last_name)
            output.append(patient.date_of_birth)
            output.append(patient.year_of_birth)
            output.append(patient.date_of_death)
            output.append(patient.year_of_death)
            output.append(patient.gender)
            output.append(patient.gender_label)
            output.append(patient.available_ethnicity)
            output.append(patient.ethnicity_label)
            output.append(get_attrs(patient, "primary_patient_number", "number"))
            output.append("Y" if patient.ukrdc else "N")
            output.append(patient.recruited_date())
            output.append(get_attrs(patient.recruited_group(), "name"))
            output.append(get_attrs(patient.recruited_group(), "code"))
            output.append(get_groups(patient, GROUP_TYPE.COHORT))
            output.append(get_groups(patient, GROUP_TYPE.HOSPITAL))

            for cohort in cohorts:
                output.append(patient.recruited_date(cohort))

            writer.writerow(output)

        return Response(f.getvalue(), content_type="text/csv")


def register_views(app):
    app.add_url_rule("/patients", view_func=PatientListView.as_view("patient_list"))
    app.add_url_rule(
        "/patients/<int:id>", view_func=PatientDetailView.as_view("patient_detail")
    )
    app.add_url_rule(
        "/patients/<int:id>", view_func=PatientDestroyView.as_view("patient_destroy")
    )
    app.add_url_rule(
        "/patients.csv", view_func=PatientListCSVView.as_view("patient_list_csv")
    )
