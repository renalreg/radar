from radar.models.groups import Group, GROUP_TYPE
from radar.pages import PAGE

from radar_fixtures.utils import add


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
    {
        'code': 'ADTKD',
        'name': 'Autosomal Dominant Tubulointerstitial Kidney Disease (FUAN)',
        'short_name': 'ADTKD (FUAN)',
        'pages': [
            PAGE.PRIMARY_DIAGNOSIS,
            PAGE.DIAGNOSES,
            PAGE.GENETICS,
            PAGE.FAMILY_HISTORY,
            PAGE.FUAN_CLINICAL_PICTURES,
            PAGE.RESULTS,
            PAGE.DIALYSIS,
            PAGE.TRANSPLANTS,
        ]
    }
]


def create_cohorts():
    for x in COHORTS:
        group = Group()
        group.type = GROUP_TYPE.COHORT
        group.code = x['code']
        group.name = x['name']
        group.short_name = x['short_name']
        group.pages = x['pages']
        add(group)
