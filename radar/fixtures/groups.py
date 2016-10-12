from radar.fixtures.cohorts import create_cohorts
from radar.fixtures.hospitals import create_hospitals
from radar.fixtures.utils import add
from radar.models.groups import (
    GROUP_CODE_RADAR,
    GROUP_CODE_NURTURE,
    GROUP_CODE_NHS,
    GROUP_CODE_CHI,
    GROUP_CODE_UKRR,
    GROUP_CODE_HSC,
    GROUP_CODE_UKRDC,
    GROUP_CODE_NHSBT,
    GROUP_CODE_BAPN,
    GROUP_TYPE,
    Group
)

GROUPS = [
    (GROUP_TYPE.SYSTEM, GROUP_CODE_RADAR, 'RaDaR', False),
    (GROUP_TYPE.SYSTEM, GROUP_CODE_NURTURE, 'NURTuRE', False),
    (GROUP_TYPE.OTHER, GROUP_CODE_NHS, 'NHS', True),
    (GROUP_TYPE.OTHER, GROUP_CODE_CHI, 'CHI', True),
    (GROUP_TYPE.OTHER, GROUP_CODE_HSC, 'HSC', True),
    (GROUP_TYPE.OTHER, GROUP_CODE_UKRR, 'UK Renal Registry', False),
    (GROUP_TYPE.OTHER, GROUP_CODE_UKRDC, 'UKRDC', False),
    (GROUP_TYPE.OTHER, GROUP_CODE_NHSBT, 'NHS Blood and Transplant', False),
    (GROUP_TYPE.OTHER, GROUP_CODE_BAPN, 'BAPN', False),
]


def create_groups():
    create_cohorts()
    create_hospitals()

    for type_, code, name, is_recruitment_number_group in GROUPS:
        group = Group()
        group.type = type_
        group.code = code
        group.name = name
        group.short_name = name
        group.is_recruitment_number_group = is_recruitment_number_group
        add(group)
