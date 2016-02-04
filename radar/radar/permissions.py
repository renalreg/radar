from radar.models.groups import GROUP_TYPE
from radar.groups import is_radar_group
from radar.roles import PERMISSION
from radar.models.source_types import SOURCE_TYPE_RADAR


def has_permission_for_patient(user, patient, permission):
    """Check that the the user has a permission on any of the groups
    they share with the patient."""

    if user.is_admin:
        grant = True
    else:
        # Groups in common with the patient
        group_users = intersect_groups_with_patient(user, patient, user_membership=True)

        # Check the user has the required permission
        grant = any(x.has_permission(permission) for x in group_users)

    return grant


def has_permission_for_user(user, other_user, permission, explicit=False):
    """Check that the the user has a permission on any of the groups
    they share with the user."""

    if user.is_admin:
        grant = True
    elif not explicit and user == other_user and permission in (PERMISSION.VIEW_USER, PERMISSION.EDIT_USER):
        # Users can view themselves
        grant = True
    elif other_user.is_admin and permission == PERMISSION.EDIT_USER:
        # Users can't edit admins
        grant = False
    else:
        # Groups in common with the user
        group_users = intersect_groups_with_user(user, other_user, user_membership=True)

        # Check the user has the required permission
        grant = any(x.has_permission(permission) for x in group_users)

        # Users with the EDIT_USER_MEMBERSHIP permission get the VIEW_USER permission
        if not grant and not explicit and permission == PERMISSION.VIEW_USER:
            grant = has_permission(user, PERMISSION.EDIT_USER_MEMBERSHIP)

    return grant


def has_permission(user, permission, group_type=None):
    """Check that the user has a permission."""

    if user.is_admin:
        grant = True
    else:
        group_users = user.group_users

        if group_type is not None:
            group_users = [x for x in group_users if x.group.type == group_type]

        grant = any(x.has_permission(permission) for x in group_users)

    return grant


def has_permission_for_group(user, group, permission, explicit=False):
    """Check that the user has a permission on a group."""

    if user.is_admin:
        return True
    else:
        # Users get permissions on the RaDaR group through their other groups
        if not explicit and is_radar_group(group) and permission in (PERMISSION.VIEW_PATIENT, PERMISSION.EDIT_PATIENT):
            return has_permission(user, permission)

        # Users get permissions on cohort groups through their hospital groups
        if (
            not explicit and
            group.type == GROUP_TYPE.COHORT and
            permission in (
                PERMISSION.VIEW_PATIENT, PERMISSION.EDIT_PATIENT,
                PERMISSION.RECRUIT_PATIENT, PERMISSION.EDIT_PATIENT_MEMBERSHIP
            ) and
            has_permission(user, permission, group_type=GROUP_TYPE.HOSPITAL)
        ):
            return True

        for group_user in user.group_users:
            # User is a member of the group and has the required permission
            if group_user.group == group and group_user.has_permission(permission):
                return True

        # User not a member of the group or doesn't have the required permission
        return False


def has_permission_for_group_role(user, group, role):
    if user.is_admin:
        return True
    else:
        for group_user in user.group_users:
            if group_user.group == group and role in group_user.managed_roles:
                return True

    return False


def intersect_groups_with_patient(user, patient, user_membership=False, patient_membership=False):
    """Find the intersection of the groups the user and patient belong to."""

    group_patients = {x.group: x for x in patient.group_patients}

    intersection = []

    for group_user in user.group_users:
        group = group_user.group
        group_patient = group_patients.get(group)

        if group_patient:
            if user_membership and patient_membership:
                intersection.append((group_user, group_patient))
            elif user_membership:
                intersection.append(group_user)
            elif patient_membership:
                intersection.append(group_patient)
            else:
                intersection.append(group_user.group)

    return intersection


def intersect_groups_with_user(user, other_user, user_membership=False, other_user_membership=False):
    """Find the intersection of the groups the patient and user belong to."""

    other_group_users = {x.group: x for x in other_user.group_users}

    intersection = []

    for group_user in user.group_users:
        group = group_user.group
        other_group_user = other_group_users.get(group)

        if other_group_user:
            if user_membership and other_user_membership:
                intersection.append((group_user, other_group_user))
            elif user_membership:
                intersection.append(group_user)
            elif other_user_membership:
                intersection.append(other_group_user)
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
        return super(PatientObjectPermission, self).has_object_permission(request, user, obj.patient)


class SourceObjectPermission(Permission):
    """Checks that the user has permission to edit an object belonging to a data source.

    Permission is granted if:
    * The user is only viewing the object. Permissions for this are handled in
      PatientObjectPermission.
    * The user is modifiying the object and the object was entered on RaDaR and
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

            # Can only modify data entered on RaDaR
            if not user.is_admin and source_type != SOURCE_TYPE_RADAR:
                return False

            # Check permissions
            if not has_permission_for_group(user, source_group, PERMISSION.EDIT_PATIENT):
                return False

            return True


class RadarSourceObjectPermission(Permission):
    """Ensures that only objects from RaDaR can be modified.

    Permission is granted:
    * The user is only viewing the object. Permissions for this are handled in
      PatientObjectPermission.
    * The user is modifying an object entered on RaDaR.
    """

    def has_object_permission(self, request, user, obj):
        if not super(RadarSourceObjectPermission, self).has_object_permission(request, user, obj):
            return False

        if is_safe_method(request):
            return True
        else:
            source_type = obj.source_type
            source_group = obj.source_group

            if not user.is_admin:
                # Can only modify data entered on RaDaR
                if source_type != SOURCE_TYPE_RADAR:
                    return False

                # Can only modify data from the RaDaR group
                if not is_radar_group(source_group):
                    return False

            # Check permissions
            if not has_permission_for_group(user, source_group, PERMISSION.EDIT_PATIENT):
                return False

            return True


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


class PatientRadarSourceObjectPermission(PatientObjectPermission, RadarSourceObjectPermission):
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

        return (
            user.is_admin and  # only admin's can delete users
            obj != user  # can't delete yourself
        )


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
        if not super(GroupPatientRetrievePermission, self).has_object_permission(request, user, obj):
            return False

        return has_permission_for_patient(user, obj.patient, PERMISSION.VIEW_USER)


class GroupPatientUpdatePermission(Permission):
    def has_object_permission(self, request, user, obj):
        if not super(GroupPatientUpdatePermission, self).has_object_permission(request, user, obj):
            return False

        return (
            has_permission_for_patient(user, obj.patient, PERMISSION.VIEW_DEMOGRAPHICS) and
            has_permission_for_group(user, obj.group, PERMISSION.EDIT_PATIENT_MEMBERSHIP)
        )


class GroupPatientDestroyPermission(Permission):
    def has_object_permission(self, request, user, obj):
        if not super(GroupPatientDestroyPermission, self).has_object_permission(request, user, obj):
            return False

        # Has the view demographics permission and explicit permission on the group or permission
        # on the group and explicit permission on the created group
        return (
            has_permission_for_patient(user, obj.patient, PERMISSION.VIEW_DEMOGRAPHICS) and
            (
                has_permission_for_group(user, obj.group, PERMISSION.EDIT_PATIENT_MEMBERSHIP, explicit=True) or
                (
                    has_permission_for_group(user, obj.group, PERMISSION.EDIT_PATIENT_MEMBERSHIP) and
                    has_permission_for_group(user, obj.created_group, PERMISSION.EDIT_PATIENT_MEMBERSHIP, explicit=True)
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

        return (
            has_permission_for_group(user, obj.group, PERMISSION.EDIT_USER_MEMBERSHIP) and
            has_permission_for_group_role(user, obj.group, obj.role)
        )


class GroupUserDestroyPermission(Permission):
    def has_object_permission(self, request, user, obj):
        if not super(GroupUserDestroyPermission, self).has_object_permission(request, user, obj):
            return False

        return (
            has_permission_for_group(user, obj.group, PERMISSION.EDIT_USER_MEMBERSHIP) and
            has_permission_for_group_role(user, obj.group, obj.role)
        )
