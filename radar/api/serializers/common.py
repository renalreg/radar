from datetime import datetime

from cornflake import fields
from cornflake import serializers
from cornflake.sqlalchemy_orm import ModelSerializer, ReferenceField
from cornflake.validators import in_
import pytz

from radar.exceptions import PermissionDenied
from radar.models.forms import Form, GroupForm
from radar.models.groups import Group, GROUP_TYPE, GroupPage
from radar.models.patients import Patient
from radar.models.source_types import (
    SOURCE_TYPE_MANUAL,
    SOURCE_TYPE_UKRDC,
    SOURCE_TYPE_BATCH,
)
from radar.models.users import User
from radar.pages import PAGE
from radar.permissions import has_permission_for_group, has_permission_for_patient
from radar.roles import PERMISSION


def lookup_field_defaults(kwargs):
    kwargs.setdefault("key_name", "id")  # Value stored in database
    kwargs.setdefault("value_name", "label")  # Value displayed to user


class StringLookupField(fields.StringLookupField):
    def __init__(self, *args, **kwargs):
        lookup_field_defaults(kwargs)
        super(StringLookupField, self).__init__(*args, **kwargs)


class IntegerLookupField(fields.IntegerLookupField):
    def __init__(self, *args, **kwargs):
        lookup_field_defaults(kwargs)
        super(IntegerLookupField, self).__init__(*args, **kwargs)


class EnumLookupField(fields.EnumLookupField):
    def __init__(self, *args, **kwargs):
        lookup_field_defaults(kwargs)
        super(EnumLookupField, self).__init__(*args, **kwargs)


class TinyUserSerializer(ModelSerializer):
    id = fields.IntegerField()
    username = fields.StringField()
    email = fields.StringField()
    first_name = fields.StringField()
    last_name = fields.StringField()

    class Meta:
        model_class = User
        fields = ("id", "username", "email", "first_name", "last_name")


class UserField(ReferenceField):
    model_class = User
    serializer_class = TinyUserSerializer


class CreatedUserField(UserField):
    def get_value(self, data):
        instance = self.root.instance

        # Set the created_user to the current_user for new records
        if instance is None:
            return self.context["user"]
        else:
            return self.get_attribute(instance)


class ModifiedUserField(UserField):
    def get_value(self, data):
        # Set the modified user to the current_user
        return self.context["user"]


class CreatedDateField(fields.DateTimeField):
    def get_value(self, data):
        instance = self.root.instance

        # Set the created_date to now for new records
        if instance is None:
            return datetime.now(pytz.utc)
        else:
            return self.get_attribute(instance)


class ModifiedDateField(fields.DateTimeField):
    def get_value(self, data):
        # Set the modified date to now
        return datetime.now(pytz.utc)


class MetaMixin(serializers.Serializer):
    created_user = CreatedUserField(required=False)
    modified_user = ModifiedUserField()
    created_date = CreatedDateField(required=False)
    modified_date = ModifiedDateField()

    def get_model_exclude(self):
        model_exclude = super(MetaMixin, self).get_model_exclude()
        model_exclude.add("created_user_id")
        model_exclude.add("modified_user_id")
        return model_exclude


class UserField(ReferenceField):
    model_class = User


class UserMixin(object):
    user = UserField()

    def get_model_exclude(self):
        attrs = super(UserMixin, self).get_model_exclude()
        attrs.add("user_id")
        return attrs


class QueryPatientField(ReferenceField):
    model_class = Patient

    def validate(self, patient):
        user = self.context["user"]

        if not has_permission_for_patient(user, patient, PERMISSION.VIEW_PATIENT):
            raise PermissionDenied()

        return patient


class PatientField(ReferenceField):
    model_class = Patient

    def validate(self, patient):
        user = self.context["user"]

        if not has_permission_for_patient(user, patient, PERMISSION.EDIT_PATIENT):
            raise PermissionDenied()

        return patient


class PatientMixin(object):
    patient = PatientField()

    def get_model_exclude(self):
        model_exclude = super(PatientMixin, self).get_model_exclude()
        model_exclude.add("patient_id")
        return model_exclude


class TinyGroupSerializer(ModelSerializer):
    type = fields.EnumField(GROUP_TYPE)

    class Meta(object):
        model_class = Group
        fields = ["id", "type", "code", "name", "short_name"]


class GroupPageSerializer(ModelSerializer):
    page = fields.EnumField(PAGE)
    weight = fields.IntegerField()

    class Meta(object):
        model_class = GroupPage
        exclude = ["group_id"]


class TinyFormSerializer(ModelSerializer):
    class Meta(object):
        model_class = Form
        fields = ["id", "name", "slug"]


class GroupFormSerializer(ModelSerializer):
    form = TinyFormSerializer()
    weight = fields.IntegerField()

    class Meta(object):
        model_class = GroupForm
        exclude = ["group_id", "form_id"]


class GroupSerializer(ModelSerializer):
    type = fields.EnumField(GROUP_TYPE)
    pages = fields.ListField(child=GroupPageSerializer(), source="group_pages")
    forms = fields.ListField(child=GroupFormSerializer(), source="group_forms")
    has_dependencies = fields.BooleanField(read_only=True)
    instructions = fields.StringField()
    is_transplant_centre = fields.BooleanField()

    class Meta(object):
        model_class = Group
        exclude = ["_instructions", "parent_group_id"]


class GroupField(ReferenceField):
    model_class = Group
    serializer_class = GroupSerializer


class TinyGroupField(ReferenceField):
    model_class = Group
    serializer_class = TinyGroupSerializer


class SourceGroupField(GroupField):
    def validate(self, group):
        user = self.context["user"]

        # Group must be a system or hospital (unless the user is an admin)
        if not user.is_admin and group.type not in (
            GROUP_TYPE.SYSTEM,
            GROUP_TYPE.HOSPITAL,
        ):
            raise PermissionDenied()

        if not has_permission_for_group(user, group, PERMISSION.EDIT_PATIENT):
            raise PermissionDenied()

        return group


class SystemSourceGroupField(GroupField):
    def validate(self, group):
        user = self.context["user"]

        # Group must be a system (unless the user is an admin)
        if not user.is_admin and group.type != GROUP_TYPE.SYSTEM:
            raise PermissionDenied()

        if not has_permission_for_group(user, group, PERMISSION.EDIT_PATIENT):
            raise PermissionDenied()

        return group


class CohortGroupField(GroupField):
    def validate(self, group):
        # Group must be a cohort
        if group.type != GROUP_TYPE.COHORT:
            raise PermissionDenied()

        return group


class SourceTypeField(fields.StringField):
    def __init__(self, **kwargs):
        kwargs.setdefault("default", SOURCE_TYPE_MANUAL)
        kwargs.setdefault(
            "validators",
            [in_([SOURCE_TYPE_MANUAL, SOURCE_TYPE_UKRDC, SOURCE_TYPE_BATCH])],
        )
        super(SourceTypeField, self).__init__(**kwargs)

    def validate(self, source_type):
        user = self.context["user"]

        # Only admins can enter data for non-manual source types
        if not user.is_admin and source_type != SOURCE_TYPE_MANUAL:
            raise PermissionDenied()

        return source_type


class SourceMixin(object):
    source_group = SourceGroupField()
    source_type = SourceTypeField()

    def get_model_exclude(self):
        model_exclude = super(SourceMixin, self).get_model_exclude()
        model_exclude.add("source_group_id")
        return model_exclude


class SystemSourceMixin(object):
    source_group = SystemSourceGroupField()
    source_type = SourceTypeField()

    def get_model_exclude(self):
        model_exclude = super(SystemSourceMixin, self).get_model_exclude()
        model_exclude.add("source_group_id")
        return model_exclude


class CohortGroupMixin(object):
    group = CohortGroupField()

    def get_model_exclude(self):
        model_exclude = super(CohortGroupMixin, self).get_model_exclude()
        model_exclude.add("group_id")
        return model_exclude

    def validate(self, data):
        data = super(CohortGroupMixin, self).validate(data)

        patient = data["patient"]
        group = data["group"]

        if not patient.in_group(group):
            raise PermissionDenied()

        return data


class TinyGroupPatientSerializer(serializers.Serializer):
    id = fields.IntegerField()
    group = TinyGroupSerializer()
    from_date = fields.DateTimeField()
    to_date = fields.DateTimeField()
    current = fields.BooleanField(read_only=True)
