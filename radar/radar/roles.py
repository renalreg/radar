from collections import OrderedDict
from enum import Enum


class ROLE(Enum):
    IT = 'IT'
    ADMIN = 'ADMIN'
    CLINICIAN = 'CLINICIAN'
    SENIOR_CLINICIAN = 'SENIOR_CLINICIAN'
    SENIOR_RESEARCHER = 'SENIOR_RESEARCHER'
    RESEARCHER = 'RESEARCHER'

    def __str__(self):
        return str(self.value)


ROLE_NAMES = OrderedDict([
    (ROLE.SENIOR_CLINICIAN, 'Senior Clinician'),
    (ROLE.CLINICIAN, 'Clinician'),
    (ROLE.ADMIN, 'Admin'),
    (ROLE.IT, 'IT'),
    (ROLE.RESEARCHER, 'Researcher'),
    (ROLE.SENIOR_RESEARCHER, 'Senior Researcher'),
])


class PERMISSION(Enum):
    VIEW_PATIENT = 'VIEW_PATIENT'
    EDIT_PATIENT = 'EDIT_PATIENT'
    RECRUIT_PATIENT = 'RECRUIT_PATIENT'
    VIEW_DEMOGRAPHICS = 'VIEW_DEMOGRAPHICS'
    VIEW_USER = 'VIEW_USER'
    EDIT_USER = 'EDIT_USER'
    EDIT_USER_MEMBERSHIP = 'EDIT_USER_MEMBERSHIP'

    def __str__(self):
        return str(self.value)


PERMISSION_ROLES = {
    PERMISSION.VIEW_PATIENT: [
        ROLE.CLINICIAN,
        ROLE.SENIOR_CLINICIAN,
        ROLE.ADMIN,
        ROLE.SENIOR_RESEARCHER,
        ROLE.RESEARCHER,
    ],
    PERMISSION.EDIT_PATIENT: [
        ROLE.CLINICIAN,
        ROLE.SENIOR_CLINICIAN,
    ],
    PERMISSION.RECRUIT_PATIENT: [
        ROLE.CLINICIAN,
        ROLE.SENIOR_CLINICIAN,
    ],
    PERMISSION.VIEW_DEMOGRAPHICS: [
        ROLE.CLINICIAN,
        ROLE.SENIOR_CLINICIAN,
        ROLE.ADMIN,
        ROLE.SENIOR_RESEARCHER,
    ],
    PERMISSION.VIEW_USER: [
        ROLE.IT,
        ROLE.ADMIN,
        ROLE.SENIOR_CLINICIAN,
    ],
}

MANAGED_ROLES = {
    ROLE.IT: [
        ROLE.CLINICIAN,
    ],
    ROLE.ADMIN: [
        ROLE.CLINICIAN,
    ],
    ROLE.SENIOR_CLINICIAN: [
        ROLE.CLINICIAN,
    ],
    ROLE.SENIOR_RESEARCHER: [
        ROLE.RESEARCHER,
    ]
}


def get_roles_managed_by_role(role):
    return MANAGED_ROLES.get(role, [])


def get_roles_with_permission(permission):
    return PERMISSION_ROLES.get(permission, [])
