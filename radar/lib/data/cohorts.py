from radar.lib.data.validation import validate
from radar.lib.database import db
from radar.lib.models import Cohort, CohortFeature, ResultGroupDefinition, CohortResultGroupDefinition

# TODO
COHORTS = [
    {
        'name': 'SRNS',
        'features': [
            ('DEMOGRAPHICS', 0),
            ('GENETICS', 1),
            ('RENAL_IMAGING', 2),
            ('SALT_WASTING_CLINICAL_FEATURES', 3),
        ],
        'result_group_definitions': [
            ('LFT', 4),
        ],
    },
    {
        'name': 'MPGN',
        'features': [
            ('DEMOGRAPHICS', 0),
            ('GENETICS', 1),
            ('RENAL_IMAGING', 2),
            ('SALT_WASTING_CLINICAL_FEATURES', 3),
        ],
        'result_group_definitions': [
            ('LFT', 4),
        ],
    },
    {
        'name': 'Salt Wasting',
        'features': [
            ('DEMOGRAPHICS', 0),
            ('GENETICS', 1),
            ('RENAL_IMAGING', 2),
            ('SALT_WASTING_CLINICAL_FEATURES', 3),
        ],
        'result_group_definitions': [
            ('LFT', 4),
        ],
    }
]


def create_cohorts():
    for x in COHORTS:
        cohort = Cohort(name=x['name'])
        cohort = validate(cohort)
        db.session.add(cohort)

        for name, weight in x['features']:
            cohort_feature = CohortFeature(
                cohort=cohort,
                name=name,
                weight=weight
            )
            db.session.add(cohort_feature)

        for code, weight in x['result_group_definitions']:
            result_group_definition = ResultGroupDefinition.query.filter(ResultGroupDefinition.code == code).one()

            cohort_result_group_definition = CohortResultGroupDefinition(
                cohort=cohort,
                result_group_definition=result_group_definition,
                weight=weight,
            )
            db.session.add(cohort_result_group_definition)
