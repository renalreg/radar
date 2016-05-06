from radar.models.groups import GroupPatient
from radar.api.serializers.group_patients import GroupPatientSerializer
from radar.api.permissions import (
    GroupPatientCreatePermission,
    GroupPatientRetrievePermission,
    GroupPatientUpdatePermission,
    GroupPatientDestroyPermission
)
from radar.api.views.generics import (
    ListModelView,
    CreateModelView,
    RetrieveModelView,
    UpdateModelView,
    DestroyModelView
)
from radar.api.views.common import (
    filter_query_by_group,
    filter_query_by_patient_permissions,
    filter_query_by_patient
)


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


class GroupPatientRetrieveView(RetrieveModelView):
    serializer_class = GroupPatientSerializer
    model_class = GroupPatient
    permission_classes = [GroupPatientRetrievePermission]


class GroupPatientUpdateView(UpdateModelView):
    serializer_class = GroupPatientSerializer
    model_class = GroupPatient
    permission_classes = [GroupPatientUpdatePermission]


class GroupPatientDestroyView(DestroyModelView):
    model_class = GroupPatient
    permission_classes = [GroupPatientDestroyPermission]


def register_views(app):
    app.add_url_rule('/group-patients', view_func=GroupPatientListView.as_view('group_patient_list'))
    app.add_url_rule('/group-patients', view_func=GroupPatientCreateView.as_view('group_patient_create'))
    app.add_url_rule('/group-patients/<int:id>', view_func=GroupPatientRetrieveView.as_view('group_patient_retrieve'))
    app.add_url_rule('/group-patients/<int:id>', view_func=GroupPatientUpdateView.as_view('group_patient_update'))
    app.add_url_rule('/group-patients/<int:id>', view_func=GroupPatientDestroyView.as_view('group_patient_destroy'))
