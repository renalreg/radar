from datetime import datetime

import pytz
from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake import fields
from cornflake.exceptions import ValidationError
from cornflake.validators import not_in_future

from radar.api.serializers.common import PatientMixin, MetaMixin, GroupField
from radar.database import db
from radar.exceptions import PermissionDenied
from radar.models.groups import GroupPatient, check_dependencies, DependencyError, GROUP_TYPE
from radar.permissions import has_permission_for_patient, has_permission_for_group
from radar.roles import PERMISSION


class GroupPatientSerializer(PatientMixin, MetaMixin, ModelSerializer):
    group = GroupField()
    from_date = fields.DateTimeField(validators=[not_in_future()])
    to_date = fields.DateTimeField(required=False, validators=[not_in_future()])
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

    def check_dependencies(self, data):
        group = data['group']
        patient = data['patient']

        groups = patient.groups

        instance = self.root.instance

        if instance is not None:
            groups.remove(instance.group)

        groups.append(group)

        try:
            check_dependencies(groups)
        except DependencyError as e:
            raise ValidationError({'group': e.message})

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

        self.check_dependencies(data)

        # Check that the patient doesn't already belong to this group
        # Note: it's important this check happens after the permission checks to prevent membership enumeration
        if self.is_duplicate(data):
            raise ValidationError({'group': 'Patient already belongs to this group.'})

        # Check the from date isn't before the date the patient was added to the system
        if not data['group'].type != GROUP_TYPE.SYSTEM:
            recruited_date = data['patient'].recruited_date()

            if recruited_date is not None and data['from_date'] < recruited_date.date():
                raise ValidationError({'from_date': "Must be on or after the recruitment date."})

        return data

    def save(self):
        group_patient = super(GroupPatientSerializer, self).save()

        patient = group_patient.patient
        parent_group = group_patient.group.parent_group

        # Add the patient to the parent group
        if parent_group is not None and not patient.in_group(parent_group, current=True):
            parent_group_patient = GroupPatient()
            parent_group_patient.patient = patient
            parent_group_patient.group = parent_group
            parent_group_patient.created_group = group_patient.created_group
            parent_group_patient.from_date = datetime.now(pytz.UTC)
            parent_group_patient.created_user = group_patient.created_user
            parent_group_patient.modified_user = group_patient.modified_user
            parent_group_patient.created_date = group_patient.created_date
            parent_group_patient.modified_date = group_patient.modified_date
            db.session.add(parent_group_patient)

        return group_patient
