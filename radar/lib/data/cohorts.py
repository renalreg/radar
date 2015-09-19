from radar.lib.data.validation import validate
from radar.lib.database import db
from radar.lib.models import Cohort, CohortFeature, ResultGroupSpec, CohortResultGroupSpec

# TODO
COHORTS = [
    {
        'code': 'INS',
        'name': 'INS',
        'features': [
            'DEMOGRAPHICS',
            'GENETICS',
            'RENAL_IMAGING',
            'SALT_WASTING_CLINICAL_FEATURES',
        ],
        'result_group_codes': [
            'LFT'
        ],
    },
    {
        'code': 'MPGN',
        'name': 'MPGN',
        'features': [
            'DEMOGRAPHICS',
            'GENETICS',
            'RENAL_IMAGING',
            'SALT_WASTING_CLINICAL_FEATURES',
        ],
        'result_group_codes': [
            'LFT',
        ],
    },
    {
        'code': 'SALT_WASTING',
        'name': 'Hypokalaemic Alkalosis',
        'features': [
            'DEMOGRAPHICS',
            'GENETICS',
            'RENAL_IMAGING',
            'SALT_WASTING_CLINICAL_FEATURES',
        ],
        'result_group_codes': [
            'LFT',
        ],
    }
]


def create_cohorts():
    for x in COHORTS:
        cohort = Cohort()
        cohort.code = x['code']
        cohort.name = x['name']
        cohort = validate(cohort)
        db.session.add(cohort)

        for i, name in enumerate(x['features']):
            cohort_feature = CohortFeature()
            cohort_feature.cohort = cohort
            cohort_feature.name = name
            cohort_feature.weight = i * 100  # leave some gaps
            cohort_feature = validate(cohort_feature)
            db.session.add(cohort_feature)

        for i, code in enumerate(x['result_group_codes']):
            result_group_spec = ResultGroupSpec.query.filter(ResultGroupSpec.code == code).one()

            cohort_result_group_spec = CohortResultGroupSpec()
            cohort_result_group_spec.cohort = cohort
            cohort_result_group_spec.result_group_spec = result_group_spec
            cohort_result_group_spec.weight = i * 100  # leave some gaps
            cohort_result_group_spec = validate(cohort_result_group_spec)
            db.session.add(cohort_result_group_spec)
