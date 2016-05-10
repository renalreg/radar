from radar.models.groups import Group, GroupPatient, GroupUser
from radar.models.patients import Patient
from radar.models.users import User


def make_groups(n):
    return [Group() for _ in range(n)]


def make_patient(groups=None):
    if groups is None:
        groups = []

    patient = Patient()

    for group in groups:
        group_patient = GroupPatient()
        group_patient.group = group
        group_patient.patient = patient

    return patient


def make_user(groups=None):
    if groups is None:
        groups = []

    user = User()

    for group in groups:
        if isinstance(group, GroupUser):
            group_user = group
        else:
            try:
                group, role = group
            except (TypeError, ValueError):
                role = None

            group_user = GroupUser()
            group_user.group = group
            group_user.user = user
            group_user.role = role

    return user
