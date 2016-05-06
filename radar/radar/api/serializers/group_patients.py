from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake import fields
from cornflake.exceptions import ValidationError

from radar.api.serializers.common import PatientMixin, MetaMixin, GroupField
from radar.models.groups import GroupPatient
from radar.permissions import has_permission_for_patient, has_permission_for_group
from radar.roles import PERMISSION
from radar.exceptions import PermissionDenied


class GroupPatientSerializer(PatientMixin, MetaMixin, ModelSerializer):
    group = GroupField()
    from_date = fields.DateField()
    to_date = fields.DateField(required=False)
    created_group = GroupField()
    current = fields.BooleanField(read_only=True)

    class Meta(object):
        model_class = GroupPatient
        exclude = ['group_id', 'created_group_id']

    def is_duplicate(self, data):
        group = data['group']
        patient = data['patient']
        instance = self.instance

        duplicate = any(
            group == x.group and
            (instance is None or instance != x)
            for x in patient.current_group_patients
        )

        return duplicate

    def validate(self, data):
        data = super(GroupPatientSerializer, self).validate(data)

        current_user = self.context['user']
        instance = self.instance

        if not has_permission_for_patient(current_user, data['patient'], PERMISSION.VIEW_DEMOGRAPHICS):
            raise PermissionDenied()

        if not has_permission_for_group(current_user, data['group'], PERMISSION.EDIT_PATIENT_MEMBERSHIP):
            raise PermissionDenied()

        check_old_created_group = (
            instance is not None and
            instance.created_group != data['created_group']
        )

        check_new_created_group = (
            instance is None or
            instance.group != data['group'] or
            instance.created_group != data['created_group']
        )

        if (
            check_old_created_group and
            not has_permission_for_group(
                current_user,
                data['created_group'],
                PERMISSION.EDIT_PATIENT_MEMBERSHIP,
                explicit=True
            )
        ) or (
            check_new_created_group and
            not has_permission_for_group(
                current_user,
                data['created_group'],
                PERMISSION.EDIT_PATIENT_MEMBERSHIP,
                explicit=True
            )
        ):
            raise PermissionDenied()

        # Check that the patient doesn't already belong to this group
        # Note: it's important this check happens after the permission checks to prevent membership enumeration
        if self.is_duplicate(data):
            raise ValidationError({'group': 'Patient already belongs to this group.'})

        return data
