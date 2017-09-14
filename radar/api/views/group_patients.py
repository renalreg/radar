from flask import jsonify, Response, request

from radar.api.permissions import (
    GroupPatientCreatePermission,
    GroupPatientDestroyPermission,
    GroupPatientRetrievePermission,
    GroupPatientUpdatePermission,
)
from radar.api.serializers.group_patients import GroupPatientSerializer
from radar.api.views.common import (
    filter_query_by_group,
    filter_query_by_patient,
    filter_query_by_patient_permissions,
)
from radar.api.views.generics import (
    CreateModelView,
    DestroyModelView,
    ListModelView,
    RetrieveModelView,
    UpdateModelView,

)
from radar.database import db
from radar.models.groups import GroupPatient
from radar.utils import camel_case_keys


class GroupPatientListView(ListModelView):
    serializer_class = GroupPatientSerializer
    model_class = GroupPatient

    def filter_query(self, query):
        query = super(GroupPatientListView, self).filter_query(query)
        query = filter_query_by_patient_permissions(query, GroupPatient)
        query = filter_query_by_patient(query, GroupPatient)
        query = filter_query_by_group(query, GroupPatient)
        return query


class GroupPatientCreateView(CreateModelView):
    serializer_class = GroupPatientSerializer
    model_class = GroupPatient
    permission_classes = [GroupPatientCreatePermission]

    def create(self, *args, **kwargs):
        json = request.get_json()

        if json is None:
            raise BadRequest()
        serializer = self.get_serializer(data=json)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()

        db.session.add(obj)
        db.session.commit()

        update_system_groups(obj.patient)

        data = serializer.data
        data = camel_case_keys(data)
        return jsonify(data), 200


class GroupPatientRetrieveView(RetrieveModelView):
    serializer_class = GroupPatientSerializer
    model_class = GroupPatient
    permission_classes = [GroupPatientRetrievePermission]


class GroupPatientUpdateView(UpdateModelView):
    serializer_class = GroupPatientSerializer
    model_class = GroupPatient
    permission_classes = [GroupPatientUpdatePermission]

    def update(self, *args, **kwargs):
        response = super(GroupPatientUpdateView, self).update(*args, **kwargs)

        obj = self.get_object()
        update_system_groups(obj.patient)

        return response


class GroupPatientDestroyView(DestroyModelView):
    model_class = GroupPatient
    permission_classes = [GroupPatientDestroyPermission]

    def delete(self, *args, **kwargs):
        obj = self.get_object()
        patient = obj.patient
        db.session.delete(obj)
        db.session.commit()

        update_system_groups(patient)

        return Response(status=200)


def last_system_group(patient):
    return len(patient.systems) == 1


def update_system_groups(patient):
    """Check that patient system group still has some children groups."""

    systems = patient.systems
    if len(systems) == 1:
        return Response(status=200)

    counter = {system: 0 for system in systems}

    for cohort in patient.cohorts:
        if cohort.parent_group in counter:
            counter[cohort.parent_group] += 1

    for system, children_number in counter.items():
        if children_number == 0:
            for group_patient in system.group_patients:
                if group_patient.patient_id == patient.id and not last_system_group(patient):
                    db.session.delete(group_patient)
                    db.session.commit()


def register_views(app):
    app.add_url_rule('/group-patients', view_func=GroupPatientListView.as_view('group_patient_list'))
    app.add_url_rule('/group-patients', view_func=GroupPatientCreateView.as_view('group_patient_create'))
    app.add_url_rule('/group-patients/<int:id>', view_func=GroupPatientRetrieveView.as_view('group_patient_retrieve'))
    app.add_url_rule('/group-patients/<int:id>', view_func=GroupPatientUpdateView.as_view('group_patient_update'))
    app.add_url_rule('/group-patients/<int:id>', view_func=GroupPatientDestroyView.as_view('group_patient_destroy'))
