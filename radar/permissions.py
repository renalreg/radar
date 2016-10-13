from radar.models.groups import GROUP_TYPE
from radar.roles import PERMISSION


def has_permission_for_patient(user, patient, permission):
    """Check that the the user has a permission on any of the groups
    they share with the patient."""

    if user.is_admin:
        grant = True
    elif permission == PERMISSION.EDIT_PATIENT and patient.frozen:
        # Can't edit frozen patients
        grant = False
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
        # Users can view and edit themselves
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
        # Users get permissions on the system groups through their other groups
        if not explicit and group.type == GROUP_TYPE.SYSTEM and permission in (PERMISSION.VIEW_PATIENT, PERMISSION.EDIT_PATIENT):
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
