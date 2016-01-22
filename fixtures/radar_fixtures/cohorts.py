from radar_fixtures.validation import validate_and_add
from radar.models.groups import Group, GROUP_TYPE
from radar.pages import PAGE

COHORTS = [
    {
        'code': 'BONEITIS',
        'name': 'Bone-itis',
        'short_name': 'Bone-itis',
        'pages': [
            PAGE.PRIMARY_DIAGNOSIS,
            PAGE.DIAGNOSES,
        ],
    },
    {
        'code': 'CIRCUSITIS',
        'name': 'Circusitis',
        'short_name': 'Circusitis',
        'pages': [
            PAGE.PRIMARY_DIAGNOSIS,
            PAGE.DIAGNOSES,
        ],
    },
]


def create_cohorts():
    for x in COHORTS:
        group = Group()
        group.type = GROUP_TYPE.COHORT
        group.code = x['code']
        group.name = x['name']
        group.short_name = x['short_name']
        group.pages = x['pages']
        group = validate_and_add(group)
