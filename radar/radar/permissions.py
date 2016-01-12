from radar.models.groups import GROUP_TYPE_HOSPITAL
from radar.groups import is_radar_group
from radar.roles import PERMISSIONS
from radar.models.source_types import SOURCE_TYPE_RADAR


def has_permission_for_patient(user, patient, permission, group_type=None):
    """Check that the the user has a permission on any of the groups
    they share with the patient."""

    if user.is_admin:
        grant = True
    else:
        # Groups in common with the patient
        group_users = intersect_patient_and_user_groups(patient, user, user_membership=True)

        if group_type is not None:
            group_users = [x for x in group_users if x.group.type == group_type]

        # Check the user has the required permission
        grant = any(x.has_permission(permission) for x in group_users)

    return grant


def has_permission_for_any_group(user, permission, group_type=None):
    """Check that the user has a permission on any group."""

    if user.is_admin:
        grant = True
    else:
        group_users = user.group_users

        if group_type is not None:
            group_users = [x for x in group_users if x.group_type == group_type]

        grant = any(x.has_permission(permission) for x in group_users)

    return grant


def has_permission_for_group(user, group, permission):
    """Check that the user has a permission on a group."""

    if user.is_admin:
        return True
    else:
        for group_user in user.group_users:
            # User is a member of the group and has the required permission
            if group_user.group == group and group_user.has_permission(permission):
                return True

        # User not a member of the group or doesn't have the required permission
        return False


def has_permission_for_group_role(user, group, role):
    if user.is_admin:
        grant = True
    else:
        grant = False

        for group_user in user.group_users:
            if group_user.group == group and role in group_user.managed_roles:
                grant = True
                break

    return grant


def can_view_patient_object(user, patient, group=None):
    """Check that the user can view an object belonging to a patient."""

    if user.is_admin:
        return True

    # Shortcut if the user has permission through their hospital
    # We don't need to check group permissions as they can view data from any group
    if has_permission_for_patient(user, patient, PERMISSIONS.VIEW_PATIENT, group_type=GROUP_TYPE_HOSPITAL):
        return True

    if not has_permission_for_patient(user, patient, PERMISSIONS.VIEW_PATIENT):
        return False

    # If the object belongs to a group we also need to check group permissions
    if group is not None and not has_permission_for_group(user, group, PERMISSIONS.VIEW_PATIENT):
        return False

    return True


def can_edit_patient_object(user, patient, source_group=None):
    """Check that the user can edit an object belonging to a patient."""

    if user.is_admin:
        return True

    if not has_permission_for_patient(user, patient, PERMISSIONS.EDIT_PATIENT):
        return False

    # If the object has a source group we also need to check permissions for the source group
    if source_group is not None and not has_permission_for_group(user, source_group, PERMISSIONS.VIEW_PATIENT):
        return False

    return True


def intersect_patient_and_user_groups(patient, user, patient_membership=False, user_membership=False):
    """Find the intersection of the groups the patient and user belong to."""

    group_patients = {x.group: x for x in patient.group_patients}

    intersection = []

    for group_user in user.group_users:
        group = group_user.group
        group_patient = group_patients.get(group)

        if group_patient:
            if patient_membership and user_membership:
                intersection.append((group_patient, group_user))
            elif patient_membership:
                intersection.append(group_patient)
            elif user_membership:
                intersection.append(group_user)
            else:
                intersection.append(group_user.group)

    return intersection


def is_safe_method(request):
    """Check if the HTTP method is safe (read-only)."""

    return request.method in ['GET', 'HEAD']


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
    * The user is an admin.
    * The user is updating the patient and they have the edit patient permission
      through their group membership.
    * The user is viewing the patient and they have the view patient permission
      through their group membership.
    """

    def has_object_permission(self, request, user, obj):
        if not super(PatientPermission, self).has_object_permission(request, user, obj):
            return False

        if user.is_admin:
            return True

        if is_safe_method(request):
            return has_permission_for_patient(user, obj, PERMISSIONS.VIEW_PATIENT)
        else:
            return has_permission_for_patient(user, obj, PERMISSIONS.EDIT_PATIENT)


class PatientObjectPermission(PatientPermission):
    """Checks that the user has permission to view or update a patient object.

    Permission is granted if:
    * The user is an admin.
    * The user is updating the object and has the edit patient permission
      through their group membership.
    * The user is viewing the object and has the view patient permission through
      their group membership.
    """

    def has_object_permission(self, request, user, obj):
        return super(PatientObjectPermission, self).has_object_permission(request, user, obj.patient)


class SourceObjectPermission(Permission):
    """Checks that the user has permission to edit an object belonging to a data source.

    Permission is granted if:
    * The user is an admin.
    * The user is updating the object and the object was entered on RaDaR and
      the user has permission to edit objects belonging to this group.
    * The user is only viewing the object. Permissions for this are handled in
      PatientObjectPermission.
    """

    def has_object_permission(self, request, user, obj):
        if not super(SourceObjectPermission, self).has_object_permission(request, user, obj):
            return False

        if user.is_admin:
            return True

        if is_safe_method(request):
            # Users can view data from data sources they aren't members of
            return True
        else:
            # Can only modify data entered on RaDaR
            if obj.source_type != SOURCE_TYPE_RADAR:
                return False

            return can_edit_patient_object(user, obj.patient, source_group=obj.source_group)


class RadarSourceObjectPermission(Permission):
    """Ensures that only objects from RaDaR can be edited.

    Permission is granted:
    * The user is an admin.
    * The user is updating an object entered on RaDaR.
    * The user is only viewing the object. This permission doesn't restrict
      which data sources a user can view.
    """

    def has_object_permission(self, request, user, obj):
        if not super(RadarSourceObjectPermission, self).has_object_permission(request, user, obj):
            return False

        if user.is_admin:
            return True

        if is_safe_method(request):
            # This permission only affects which objects can be edited
            return True
        else:
            # Can only modify RaDaR data
            return (
                is_radar_group(obj.source_group) and
                obj.source_type == SOURCE_TYPE_RADAR
            )


class GroupObjectPermission(Permission):
    """Checks that the user has permission to view an object belonging to a group.

    Permission is granted if:
    * The user is an admin.
    * The user is attempting to update the object. The GroupObjectPermission
      should be used in conjunction with the PatientObjectPermission. The
      PatientObjectPermission checks that the user has permission to edit the
      patient.
    * The object is being viewed and the user has permission to view this
      patient and they also have permission to view the object's group. If the
      user can view the patient through their hospital group membership they can
      view data belonging to any cohort group. Otherwise the patient and user
      need to be in the same group and the user needs to also have the view
      patient permission for that group.
    """

    def has_object_permission(self, request, user, obj):
        if not super(GroupObjectPermission, self).has_object_permission(request, user, obj):
            return False

        if user.is_admin:
            return True

        if is_safe_method(request):
            patient = obj.patient

            # User isn't allowed to view this patient
            if not has_permission_for_patient(user, patient, PERMISSIONS.VIEW_PATIENT):
                return False

            group = obj.group

            # Check the user has the view patient permission for the object's
            # group. This prevents users viewing data from other groups even
            # if they have permission to view the patient.
            return can_view_patient_object(user, patient, group=group)
        else:
            # The GroupObjectPermission class should be used with the
            # PatientObjectPermission class. The PatientObjectPermission class
            # will check the user has permission to edit this patient's data.
            return True


class PatientSourceObjectPermission(PatientObjectPermission, SourceObjectPermission):
    pass


class PatientRadarSourceObjectPermission(PatientObjectPermission, RadarSourceObjectPermission):
    pass


class PatientGroupObjectPermission(PatientObjectPermission, GroupObjectPermission):
    pass


class UserListPermission(Permission):
    def has_permission(self, request, user):
        if not super(UserListPermission, self).has_permission(request, user):
            return False

        if is_safe_method(request):
            return True
        else:
            return (
                user.is_admin or
                has_permission_for_any_group(user, PERMISSIONS.EDIT_USER_MEMBERSHIP)
            )


class UserDetailPermission(Permission):
    def has_object_permission(self, request, user, obj):
        if not super(UserDetailPermission, self).has_object_permission(request, user, obj):
            return False

        return (
            user.is_admin or
            user == obj or
            has_permission_for_any_group(user, PERMISSIONS.EDIT_USER_MEMBERSHIP)
        )


class RecruitPatientPermission(Permission):
    def has_permission(self, request, user):
        if not super(RecruitPatientPermission, self).has_permission(request, user):
            return False

        return (
            user.is_admin or
            has_permission_for_any_group(user, PERMISSIONS.RECRUIT_PATIENT)
        )


class GroupPatientPermission(Permission):
    def has_object_permission(self, request, user, obj):
        if not super(GroupPatientPermission, self).has_object_permission(request, user, obj):
            return False

        if is_safe_method(request):
            return True
        else:
            # Not allowed to remove patient's from the RaDaR group
            return not is_radar_group(obj.group)
