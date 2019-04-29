from radar.models.groups import check_dependencies, DependencyError, GROUP_TYPE
from radar.models.source_types import SOURCE_TYPE_MANUAL
from radar.permissions import (
    has_permission,
    has_permission_for_group,
    has_permission_for_group_role,
    has_permission_for_patient,
    has_permission_for_user,
)
from radar.roles import PERMISSION


def is_safe_method(request):
    """Check if the HTTP method is safe (read-only)."""

    return request.method in ["GET", "HEAD"]


class Permission(object):
    def has_permission(self, request, user):
        return True

    def has_object_permission(self, request, user, obj):
        return True


class AdminPermission(Permission):
    """Checks that the user is an admin."""

    def has_permission(self, request, user):
        if not super(AdminPermission, self).has_permission(request, user):
            return False

        return user.is_admin

    def has_object_permission(self, request, user, obj):
        if not super(AdminPermission, self).has_object_permission(request, user, obj):
            return False

        return self.has_permission(request, user)


class AdminWritePermission(Permission):
    """Checks that the user is an admin for unsafe (write) requests."""

    def has_permission(self, request, user):
        if not super(AdminWritePermission, self).has_permission(request, user):
            return False

        return is_safe_method(request) or user.is_admin

    def has_object_permission(self, request, user, obj):
        if not super(AdminWritePermission, self).has_object_permission(request, user, obj):
            return False

        return self.has_permission(request, user)


class PatientPermission(Permission):
    """Checks that the user can view or update a patient.

    Permission is granted if:
    * The user is viewing the patient and they have the view patient permission
      through their group membership.
    * The user is updating the patient and they have the edit patient permission
      through their group membership.
    """

    def has_object_permission(self, request, user, obj):
        if not super(PatientPermission, self).has_object_permission(request, user, obj):
            return False

        if is_safe_method(request):
            return has_permission_for_patient(user, obj, PERMISSION.VIEW_PATIENT)
        else:
            return has_permission_for_patient(user, obj, PERMISSION.EDIT_PATIENT)


class PatientObjectPermission(PatientPermission):
    """Checks that the user has permission to view or update a patient object.

    Permission is granted if:
    * The user is viewing the object and has the view patient permission through
      their group membership.
    * The user is modifiying the object and has the edit patient permission
      through their group membership.
    """

    def has_object_permission(self, request, user, obj):
        return super(PatientObjectPermission, self).has_object_permission(
            request, user, obj.patient
        )


class SourceObjectPermission(Permission):
    """Checks that the user has permission to edit an object belonging to a data source.

    Permission is granted if:
    * The user is only viewing the object. Permissions for this are handled in
      PatientObjectPermission.
    * The user is modifiying the object and the object was manually entered and
      the user has permission to edit objects belonging to this group.
    """

    def has_object_permission(self, request, user, obj):
        if not super(SourceObjectPermission, self).has_object_permission(request, user, obj):
            return False

        if is_safe_method(request):
            return True
        else:
            source_type = obj.source_type
            source_group = obj.source_group

            # Can only modify manually entered data
            if not user.is_admin and source_type != SOURCE_TYPE_MANUAL:
                return False

            # Check permissions
            if not has_permission_for_group(user, source_group, PERMISSION.EDIT_PATIENT):
                return False

            return True


class SystemSourceObjectPermission(Permission):
    """Ensures that only objects from a system group can be modified.

    Permission is granted:
    * The user is only viewing the object. Permissions for this are handled in
      PatientObjectPermission.
    * The user is modifying an object from a system group.
    """

    def has_object_permission(self, request, user, obj):
        if not super(SystemSourceObjectPermission, self).has_object_permission(request, user, obj):
            return False

        if is_safe_method(request):
            return True
        else:
            source_type = obj.source_type
            source_group = obj.source_group

            if not user.is_admin:
                # Can only modify manually entered data
                if source_type != SOURCE_TYPE_MANUAL:
                    return False

                # Can only modify data from a system group
                if source_group.type != GROUP_TYPE.SYSTEM:
                    return False

            # Check permissions
            if not has_permission_for_group(user, source_group, PERMISSION.EDIT_PATIENT):
                return False

            return True


class GroupPermission(Permission):
    """Check that user has permission to view a group."""

    def has_object_permission(self, request, user, obj):
        if not super(GroupPermission, self).has_object_permission(request, user, obj):
            return False

        if obj.type == GROUP_TYPE.COHORT:
            permission = PERMISSION.VIEW_COHORT
        elif obj.type == GROUP_TYPE.HOSPITAL:
            permission = PERMISSION.VIEW_HOSPITAL
        else:
            return False
        return has_permission_for_group(user, obj, permission)


class GroupObjectPermission(Permission):
    """Checks that the user has permission to view an object belonging to a group.

    Permission is granted if:
    * The object is being viewed and the user has permission to view this
      patient and they also have permission to view the object's group. If the
      user can view the patient through their hospital group membership they can
      view data belonging to any cohort group. Otherwise the patient and user
      need to be in the same group and the user needs to also have the view
      patient permission for that group.
    * The user is attempting to modify the object. The GroupObjectPermission
      should be used in conjunction with the PatientObjectPermission. The
      PatientObjectPermission checks that the user has permission to edit the
      patient.
    """

    def has_object_permission(self, request, user, obj):
        if not super(GroupObjectPermission, self).has_object_permission(request, user, obj):
            return False

        group = obj.group

        if is_safe_method(request):
            permission = PERMISSION.VIEW_PATIENT
        else:
            permission = PERMISSION.EDIT_PATIENT

        if has_permission_for_group(user, group, permission):
            return True

        return False


class PatientSourceObjectPermission(PatientObjectPermission, SourceObjectPermission):
    pass


class PatientSystemSourceObjectPermission(PatientObjectPermission, SystemSourceObjectPermission):
    pass


class PatientGroupObjectPermission(PatientObjectPermission, GroupObjectPermission):
    pass


class UserCreatePermission(Permission):
    def has_permission(self, request, user):
        if not super(UserCreatePermission, self).has_permission(request, user):
            return False

        return has_permission(user, PERMISSION.EDIT_USER_MEMBERSHIP)


class UserRetrievePermission(Permission):
    def has_object_permission(self, request, user, obj):
        if not super(UserRetrievePermission, self).has_object_permission(request, user, obj):
            return False

        return has_permission_for_user(user, obj, PERMISSION.VIEW_USER)


class UserUpdatePermission(Permission):
    def has_object_permission(self, request, user, obj):
        if not super(UserUpdatePermission, self).has_object_permission(request, user, obj):
            return False

        return has_permission_for_user(user, obj, PERMISSION.EDIT_USER)


class UserDestroyPermission(Permission):
    def has_object_permission(self, request, user, obj):
        if not super(UserDestroyPermission, self).has_object_permission(request, user, obj):
            return False

        # only admin's can delete users
        # can't delete yourself
        return user.is_admin and obj != user


class RecruitPatientPermission(Permission):
    def has_permission(self, request, user):
        if not super(RecruitPatientPermission, self).has_permission(request, user):
            return False

        return has_permission(user, PERMISSION.RECRUIT_PATIENT)


class GroupPatientCreatePermission(Permission):
    def has_permission(self, request, user):
        if not super(GroupPatientCreatePermission, self).has_permission(request, user):
            return False

        return has_permission(user, PERMISSION.EDIT_PATIENT_MEMBERSHIP)


class GroupPatientRetrievePermission(Permission):
    def has_object_permission(self, request, user, obj):
        if not super(GroupPatientRetrievePermission, self).has_object_permission(
            request, user, obj
        ):
            return False

        return has_permission_for_patient(user, obj.patient, PERMISSION.VIEW_USER)


class GroupPatientUpdatePermission(Permission):
    def has_object_permission(self, request, user, obj):
        if not super(GroupPatientUpdatePermission, self).has_object_permission(request, user, obj):
            return False

        return has_permission_for_patient(
            user, obj.patient, PERMISSION.VIEW_DEMOGRAPHICS
        ) and has_permission_for_group(user, obj.group, PERMISSION.EDIT_PATIENT_MEMBERSHIP)


class GroupPatientDestroyPermission(Permission):
    def has_object_permission(self, request, user, obj):
        if not super(GroupPatientDestroyPermission, self).has_object_permission(
            request, user, obj
        ):
            return False

        patient = obj.patient
        groups = patient.groups
        groups.remove(obj.group)

        # Check deleting this group wouldn't break any dependencies
        try:
            check_dependencies(groups)
        except DependencyError:
            return False

        # Has the view demographics permission and explicit permission on the group or permission
        # on the group and explicit permission on the created group
        return has_permission_for_patient(user, obj.patient, PERMISSION.VIEW_DEMOGRAPHICS) and (
            has_permission_for_group(
                user, obj.group, PERMISSION.EDIT_PATIENT_MEMBERSHIP, explicit=True
            )
            or (
                has_permission_for_group(user, obj.group, PERMISSION.EDIT_PATIENT_MEMBERSHIP)
                and has_permission_for_group(
                    user, obj.created_group, PERMISSION.EDIT_PATIENT_MEMBERSHIP, explicit=True
                )
            )
        )


class GroupUserCreatePermission(Permission):
    def has_permission(self, request, user):
        if not super(GroupUserCreatePermission, self).has_permission(request, user):
            return False

        return has_permission(user, PERMISSION.EDIT_USER_MEMBERSHIP)


class GroupUserRetrievePermission(Permission):
    def has_object_permission(self, request, user, obj):
        if not super(GroupUserRetrievePermission, self).has_object_permission(request, user, obj):
            return False

        return has_permission_for_user(user, obj.user, PERMISSION.VIEW_USER)


class GroupUserUpdatePermission(Permission):
    def has_object_permission(self, request, user, obj):
        if not super(GroupUserUpdatePermission, self).has_object_permission(request, user, obj):
            return False

        return has_permission_for_group(
            user, obj.group, PERMISSION.EDIT_USER_MEMBERSHIP
        ) and has_permission_for_group_role(user, obj.group, obj.role)


class GroupUserDestroyPermission(Permission):
    def has_object_permission(self, request, user, obj):
        if not super(GroupUserDestroyPermission, self).has_object_permission(request, user, obj):
            return False

        return has_permission_for_group(
            user, obj.group, PERMISSION.EDIT_USER_MEMBERSHIP
        ) and has_permission_for_group_role(user, obj.group, obj.role)
