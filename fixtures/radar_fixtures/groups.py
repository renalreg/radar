from radar_fixtures.cohorts import create_cohorts
from radar_fixtures.hospitals import create_hospitals
from radar.models.groups import GROUP_CODE_RADAR, GROUP_CODE_NHS, GROUP_CODE_CHI,\
    GROUP_CODE_UKRR, GROUP_CODE_HANDC, GROUP_CODE_UKRDC, GROUP_CODE_NHSBT,\
    GROUP_CODE_BAPN, GROUP_TYPE_OTHER, Group
from radar_fixtures.validation import validate_and_add

OTHER_GROUPS = [
    (GROUP_CODE_RADAR, 'RaDaR'),
    (GROUP_CODE_NHS, 'NHS'),
    (GROUP_CODE_CHI, 'CHI'),
    (GROUP_CODE_UKRR, 'UK Renal Registry'),
    (GROUP_CODE_HANDC, 'H&C'),
    (GROUP_CODE_UKRDC, 'UKRDC'),
    (GROUP_CODE_NHSBT, 'NHS Blood and Transplant'),
    (GROUP_CODE_BAPN, 'BAPN'),
]


def create_groups():
    create_cohorts()
    create_hospitals()

    for code, name in OTHER_GROUPS:
        group = Group()
        group.type = GROUP_TYPE_OTHER
        group.code = code
        group.name = name
        group.short_name = name
        group = validate_and_add(group)
