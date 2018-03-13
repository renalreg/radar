from collections import OrderedDict
from enum import Enum

from radar.config import config


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
    RECRUIT_PATIENT = 'RECRUIT_PATIENT'
    VIEW_PATIENT = 'VIEW_PATIENT'
    VIEW_DEMOGRAPHICS = 'VIEW_DEMOGRAPHICS'
    EDIT_PATIENT = 'EDIT_PATIENT'
    EDIT_PATIENT_MEMBERSHIP = 'EDIT_PATIENT_MEMBERSHIP'
    EDIT_CONSENT = 'EDIT_CONSENT'

    VIEW_USER = 'VIEW_USER'
    EDIT_USER = 'EDIT_USER'
    EDIT_USER_MEMBERSHIP = 'EDIT_USER_MEMBERSHIP'

    def __str__(self):
        return str(self.value)


PERMISSION_ROLES = {
    PERMISSION.RECRUIT_PATIENT: [
        ROLE.CLINICIAN,
        ROLE.SENIOR_CLINICIAN,
    ],
    PERMISSION.VIEW_PATIENT: [
        ROLE.CLINICIAN,
        ROLE.SENIOR_CLINICIAN,
        ROLE.ADMIN,
        ROLE.SENIOR_RESEARCHER,
        ROLE.RESEARCHER,
    ],
    PERMISSION.VIEW_DEMOGRAPHICS: [
        ROLE.CLINICIAN,
        ROLE.SENIOR_CLINICIAN,
        ROLE.ADMIN,
        ROLE.SENIOR_RESEARCHER,
    ],
    PERMISSION.EDIT_PATIENT: [
        ROLE.CLINICIAN,
        ROLE.SENIOR_CLINICIAN,
    ],
    PERMISSION.EDIT_PATIENT_MEMBERSHIP: [
        ROLE.CLINICIAN,
        ROLE.SENIOR_CLINICIAN,
    ],
    PERMISSION.EDIT_CONSENT: [
        ROLE.CLINICIAN,
        ROLE.SENIOR_CLINICIAN,
    ],
    PERMISSION.VIEW_USER: [
        ROLE.IT,
        ROLE.ADMIN,
        ROLE.SENIOR_CLINICIAN,
        ROLE.SENIOR_RESEARCHER,
    ],
    PERMISSION.EDIT_USER: [
        ROLE.IT,
        ROLE.ADMIN,
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

READ_ONLY_PERMISSIONS = [
    PERMISSION.VIEW_PATIENT,
    PERMISSION.VIEW_DEMOGRAPHICS,
    PERMISSION.VIEW_USER,
]


def get_roles_managed_by_role(role):
    if config['READ_ONLY']:
        return []
    else:
        return MANAGED_ROLES.get(role, [])


def get_roles_with_permission(permission):
    if config['READ_ONLY'] and permission not in READ_ONLY_PERMISSIONS:
        return []
    else:
        return PERMISSION_ROLES.get(permission, [])
