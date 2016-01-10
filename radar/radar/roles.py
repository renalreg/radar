from collections import OrderedDict
from enum import Enum


class ROLES(Enum):
    IT = 'IT'
    ADMIN = 'ADMIN'
    CLINICIAN = 'CLINICIAN'
    SENIOR_CLINICIAN = 'SENIOR_CLINICIAN'
    SENIOR_RESEARCHER = 'SENIOR_RESEARCHER'
    RESEARCHER = 'RESEARCHER'

    def __str__(self):
        return str(self.value)


ROLE_NAMES = OrderedDict([
    (ROLES.SENIOR_CLINICIAN, 'Senior Clinician'),
    (ROLES.CLINICIAN, 'Clinician'),
    (ROLES.ADMIN, 'Admin'),
    (ROLES.IT, 'IT'),
    (ROLES.RESEARCHER, 'Researcher'),
    (ROLES.SENIOR_RESEARCHER, 'Senior Researcher'),
])


class PERMISSIONS(Enum):
    VIEW_PATIENT = 'VIEW_PATIENT'
    EDIT_PATIENT = 'EDIT_PATIENT'
    RECRUIT_PATIENT = 'RECRUIT_PATIENT'
    VIEW_DEMOGRAPHICS = 'VIEW_DEMOGRAPHICS'
    VIEW_USER = 'VIEW_USER'
    EDIT_USER_MEMBERSHIP = 'EDIT_USER_MEMBERSHIP'

    def __str__(self):
        return str(self.value)


PERMISSION_ROLES = {
    PERMISSIONS.VIEW_PATIENT: [
        ROLES.CLINICIAN,
        ROLES.SENIOR_CLINICIAN,
        ROLES.ADMIN,
        ROLES.SENIOR_RESEARCHER,
        ROLES.RESEARCHER,
    ],
    PERMISSIONS.EDIT_PATIENT: [
        ROLES.CLINICIAN,
        ROLES.SENIOR_CLINICIAN,
    ],
    PERMISSIONS.RECRUIT_PATIENT: [
        ROLES.CLINICIAN,
        ROLES.SENIOR_CLINICIAN,
    ],
    PERMISSIONS.VIEW_DEMOGRAPHICS: [
        ROLES.CLINICIAN,
        ROLES.SENIOR_CLINICIAN,
        ROLES.ADMIN,
        ROLES.SENIOR_RESEARCHER,
    ],
    PERMISSIONS.VIEW_USER: [
        ROLES.IT,
        ROLES.ADMIN,
        ROLES.SENIOR_CLINICIAN,
    ],
}

MANAGED_ROLES = {
    ROLES.IT: [
        ROLES.CLINICIAN,
    ],
    ROLES.ADMIN: [
        ROLES.CLINICIAN,
    ],
    ROLES.SENIOR_CLINICIAN: [
        ROLES.CLINICIAN,
    ],
    ROLES.SENIOR_RESEARCHER: [
        ROLES.RESEARCHER,
    ]
}


def get_roles_managed_by_role(role):
    return MANAGED_ROLES.get(role, [])


def get_roles_with_permission(permission):
    return PERMISSION_ROLES.get(permission, [])
