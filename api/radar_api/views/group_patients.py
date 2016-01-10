from radar_api.serializers.group_patients import GroupPatientSerializer
from radar.models.groups import GroupPatient
from radar.validation.group_patients import GroupPatientValidation
from radar.views.core import RetrieveUpdateDestroyModelView, ListCreateModelView
from radar.permissions import GroupPatientPermission


class GroupPatientListView(ListCreateModelView):
    serializer_class = GroupPatientSerializer
    model_class = GroupPatient
    validation_class = GroupPatientValidation
    permission_classes = [GroupPatientPermission]


class GroupPatientDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = GroupPatientSerializer
    model_class = GroupPatient
    validation_class = GroupPatientValidation
    permission_classes = [GroupPatientPermission]


def register_views(app):
    app.add_url_rule('/group-patients', view_func=GroupPatientListView.as_view('group_patient_list'))
    app.add_url_rule('/group-patients/<int:id>', view_func=GroupPatientDetailView.as_view('group_patient_detail'))
