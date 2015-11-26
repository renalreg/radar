from radar.fixtures.validation import validate_and_add
from radar.models import Cohort, CohortFeature, ResultGroupSpec, CohortResultGroupSpec

COHORTS = [
    {
        'code': 'RADAR',
        'name': 'RaDaR',
        'short_name': 'RaDaR',
        'features': [
            'DEMOGRAPHICS',
            'COHORTS',
            'UNITS'
        ],
        'result_group_codes': [],
    },
    {
        'code': 'ALPORT',
        'name': 'Alport Syndrome',
        'short_name': 'Alport',
        'features': [
            'DEMOGRAPHICS',
            'DIAGNOSES',
            'GENETICS',
            'FAMILY_HISTORY',
            'RESULTS',
        ],
        'result_group_codes': [],
    },
    {
        'code': 'APRT',
        'name': 'APRT Deficiency',
        'short_name': 'APRT',
        'features': [
            'DEMOGRAPHICS',
            'DIAGNOSES',
            'GENETICS',
            'FAMILY_HISTORY',
            'COMORBIDITIES',
            'RENAL_IMAGING',
            'PATHOLOGY',
            'RESULTS',
            'MEDICATIONS',
            'DIALYSIS',
            'TRANSPLANTS',
        ],
        'result_group_codes': [],
    },
    {
        'code': 'ARPKD',
        'name': 'Autosomal Recessive Polycystic Kidney Disease',
        'short_name': 'ARPKD',
        'features': [
            'DEMOGRAPHICS',
            'DIAGNOSES',
            'COMORBIDITIES',
            'RENAL_IMAGING',
            'PATHOLOGY',
            'RESULTS',
            'MEDICATIONS',
            'DIALYSIS',
            'TRANSPLANTS',
        ],
        'result_group_codes': [],
    },
    {
        'code': 'AHUS',
        'name': 'Atypical Haemolytic Uraemic Syndrome',
        'short_name': 'AHUS',
        'features': [
            'DEMOGRAPHICS',
            'DIAGNOSES',
            'COMORBIDITIES',
            'RESULTS',
            'MEDICATIONS',
            'DIALYSIS',
            'PLASMAPHERESIS',
            'TRANSPLANTS',
        ],
        'result_group_codes': [],
    },
    {
        'code': 'CALCIP',
        'name': 'Calciphylaxis',
        'short_name': 'Calciphylaxis',
        'features': [
            'DEMOGRAPHICS',
            'DIAGNOSES',
            'COMORBIDITIES',
            'RESULTS',
        ],
        'result_group_codes': [],
    },
    {
        'code': 'CYSTIN',
        'name': 'Cystinosis',
        'short_name': 'Cystinosis',
        'features': [
            'DEMOGRAPHICS',
            'DIAGNOSES',
            'MEDICATIONS',
            'DIALYSIS',
            'TRANSPLANTS',
            'HOSPITALISATIONS',
        ],
        'result_group_codes': [],
    },
    {
        'code': 'CYSURIA',
        'name': 'Cystinuria',
        'short_name': 'Cystinuria',
        'features': [
            'DEMOGRAPHICS',
            'DIAGNOSES',
        ],
        'result_group_codes': [],
    },
    {
        'code': 'DENTLOWE',
        'name': 'Dent Disease and Lowe Syndrome',
        'short_name': 'Dent & Lowe',
        'features': [
            'DEMOGRAPHICS',
            'DIAGNOSES',
        ],
        'result_group_codes': [],
    },
    {
        'code': 'FUAN',
        'name': 'Familial Urate Associated Nephropathy',
        'short_name': 'FUAN',
        'features': [
            'DEMOGRAPHICS',
            'DIAGNOSES',
            'GENETICS',
            'RENAL_IMAGING',
            'RESULTS',
            'MEDICATIONS',
        ],
        'result_group_codes': [],
    },
    {
        'code': 'HNF1B',
        'name': 'HNF1b Mutations',
        'short_name': 'HNF1b',
        'features': [
            'DEMOGRAPHICS',
            'DIAGNOSES',
            'FAMILY_HISTORY',
            'RENAL_IMAGING',
            'PATHOLOGY',
        ],
        'result_group_codes': [],
    },
    {
        'code': 'HYPERRDG',
        'name': 'Hyperoxaluria',
        'short_name': 'Hyperoxaluria',
        'features': [
            'DEMOGRAPHICS',
            'DIAGNOSES',
            'GENETICS',
            'RENAL_IMAGING',
            'RESULTS',
            'MEDICATIONS',
            'DIALYSIS',
            'TRANSPLANTS',
        ],
        'result_group_codes': [],
    },
    {
        'code': 'HYPALK',
        'name': 'Hypokalaemic Alkalosis',
        'short_name': 'Hypokalaemic Alkalosis',
        'features': [
            'DEMOGRAPHICS',
            'DIAGNOSES',
            'COMORBIDITIES',
            'RENAL_IMAGING',
            'RESULTS',
            'SALT_WASTING_CLINICAL_FEATURES',
            'MEDICATIONS',
            'DIALYSIS',
        ],
        'result_group_codes': [],
    },
    {
        'code': 'INS',
        'name': 'Idiopathic Nephrotic Syndrome',
        'short_name': 'INS',
        'features': [
            'DEMOGRAPHICS',
            'DIAGNOSES',
            'GENETICS',
            'FAMILY_HISTORY',
            'COMORBIDITIES',
            'PATHOLOGY',
            'RESULTS',
            'MEDICATIONS',
            'DIALYSIS',
            'PLASMAPHERESIS',
            'TRANSPLANTS',
            'HOSPITALISATIONS',
        ],
        'result_group_codes': [],
    },
    {
        'code': 'IGANEPHRO',
        'name': 'IgA Nephropathy',
        'short_name': 'IgA',
        'features': [
            'DEMOGRAPHICS',
            'DIAGNOSES',
        ],
        'result_group_codes': [],
    },
    {
        'code': 'MPGN',
        'name': 'Membranoproliferative Glomerulonephritis / Dense Deposit Disease',
        'short_name': 'MPGN',
        'features': [
            'DEMOGRAPHICS',
            'DIAGNOSES',
            'GENETICS',
            'FAMILY_HISTORY',
            'COMORBIDITIES',
            'PATHOLOGY',
            'RESULTS',
            'MEDICATIONS',
            'DIALYSIS',
            'TRANSPLANTS',
            'HOSPITALISATIONS',
        ],
        'result_group_codes': [],
    },
    {
        'code': 'MEMRDG',
        'name': 'Membranous Nephropathy',
        'short_name': 'Membranous Nephropathy',
        'features': [
            'DEMOGRAPHICS',
            'DIAGNOSES',
        ],
        'result_group_codes': [],
    },
    {
        'code': 'NEPHROS',
        'name': 'NephroS',
        'short_name': 'NephroS',
        'features': [
            'DEMOGRAPHICS',
            'RESULTS',
        ],
        'result_group_codes': [],
    },
    {
        'code': 'OBS',
        'name': 'Pregnancy',
        'short_name': 'Pregnancy',
        'features': [
            'DEMOGRAPHICS',
            'DIAGNOSES',
            'COMORBIDITIES',
            'PATHOLOGY',
            'RESULTS',
            'MEDICATIONS',
            'DIALYSIS',
            'PLASMAPHERESIS',
            'TRANSPLANTS',
            'HOSPITALISATIONS',
        ],
        'result_group_codes': [],
    },
    {
        'code': 'PCRA',
        'name': 'Pure Red Cell Aplasia',
        'short_name': 'PCRA',
        'features': [
            'DEMOGRAPHICS',
            'DIAGNOSES',
        ],
        'result_group_codes': [],
    },
    {
        'code': 'STECHUS',
        'name': 'STEC-associated HUS',
        'short_name': 'STEC-HUS',
        'features': [
            'DEMOGRAPHICS',
            'DIAGNOSES',
            'GENETICS',
            'FAMILY_HISTORY',
            'COMORBIDITIES',
            'RESULTS',
            'DIALYSIS',
            'PLASMAPHERESIS',
            'TRANSPLANTS',
        ],
        'result_group_codes': [],
    },
    {
        'code': 'VASRDG',
        'name': 'Vasculitis',
        'short_name': 'Vasculitis',
        'features': [
            'DEMOGRAPHICS',
            'DIAGNOSES',
            'COMORBIDITIES',
            'RENAL_IMAGING',
            'PATHOLOGY',
            'RESULTS',
            'MEDICATIONS',
            'TRANSPLANTS',
        ],
        'result_group_codes': [],
    },
]


def create_cohorts():
    for x in COHORTS:
        cohort = Cohort()
        cohort.code = x['code']
        cohort.name = x['name']
        cohort.short_name = x['short_name']
        cohort = validate_and_add(cohort)

        for i, name in enumerate(x['features']):
            cohort_feature = CohortFeature()
            cohort_feature.cohort = cohort
            cohort_feature.name = name
            cohort_feature.weight = i * 100  # leave some gaps
            validate_and_add(cohort_feature)

        for i, code in enumerate(x['result_group_codes']):
            result_group_spec = ResultGroupSpec.query.filter(ResultGroupSpec.code == code).one()

            cohort_result_group_spec = CohortResultGroupSpec()
            cohort_result_group_spec.cohort = cohort
            cohort_result_group_spec.result_group_spec = result_group_spec
            cohort_result_group_spec.weight = i * 100  # leave some gaps
            validate_and_add(cohort_result_group_spec)
