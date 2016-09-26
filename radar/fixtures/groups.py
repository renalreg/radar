from radar.fixtures.cohorts import create_cohorts
from radar.fixtures.hospitals import create_hospitals
from radar.fixtures.utils import add
from radar.models.groups import (
    GROUP_CODE_RADAR,
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

OTHER_GROUPS = [
    (GROUP_CODE_RADAR, 'RaDaR', False),
    (GROUP_CODE_NHS, 'NHS', True),
    (GROUP_CODE_CHI, 'CHI', True),
    (GROUP_CODE_HSC, 'HSC', True),
    (GROUP_CODE_UKRR, 'UK Renal Registry', False),
    (GROUP_CODE_UKRDC, 'UKRDC', False),
    (GROUP_CODE_NHSBT, 'NHS Blood and Transplant', False),
    (GROUP_CODE_BAPN, 'BAPN', False),
]


def create_groups():
    create_cohorts()
    create_hospitals()

    for code, name, is_recruitment_number_group in OTHER_GROUPS:
        group = Group()
        group.type = GROUP_TYPE.OTHER
        group.code = code
        group.name = name
        group.short_name = name
        group.is_recruitment_number_group = is_recruitment_number_group
        add(group)
