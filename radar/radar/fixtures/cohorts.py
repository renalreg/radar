from radar.fixtures.validation import validate_and_add
from radar.models import Cohort, CohortFeature, ResultGroupSpec, CohortResultGroupSpec
from radar.features import FEATURES

COHORTS = [
    {
        'code': 'RADAR',
        'name': 'RaDaR',
        'short_name': 'RaDaR',
        'features': [
            FEATURES.DEMOGRAPHICS,
            FEATURES.COHORTS,
            FEATURES.UNITS
        ],
        'result_group_codes': [],
    },
    {
        'code': 'ALPORT',
        'name': 'Alport Syndrome',
        'short_name': 'Alport',
        'features': [
            FEATURES.DIAGNOSES,
            FEATURES.GENETICS,
            FEATURES.FAMILY_HISTORY,
            FEATURES.RESULTS,
        ],
        'result_group_codes': [],
    },
    {
        'code': 'APRT',
        'name': 'APRT Deficiency',
        'short_name': 'APRT',
        'features': [
            FEATURES.DIAGNOSES,
            FEATURES.GENETICS,
            FEATURES.FAMILY_HISTORY,
            FEATURES.COMORBIDITIES,
            FEATURES.RENAL_IMAGING,
            FEATURES.PATHOLOGY,
            FEATURES.RESULTS,
            FEATURES.MEDICATIONS,
            FEATURES.DIALYSIS,
            FEATURES.TRANSPLANTS,
        ],
        'result_group_codes': [],
    },
    {
        'code': 'ARPKD',
        'name': 'Autosomal Recessive Polycystic Kidney Disease',
        'short_name': 'ARPKD',
        'features': [
            FEATURES.DIAGNOSES,
            FEATURES.COMORBIDITIES,
            FEATURES.RENAL_IMAGING,
            FEATURES.PATHOLOGY,
            FEATURES.RESULTS,
            FEATURES.MEDICATIONS,
            FEATURES.DIALYSIS,
            FEATURES.TRANSPLANTS,
        ],
        'result_group_codes': [],
    },
    {
        'code': 'AHUS',
        'name': 'Atypical Haemolytic Uraemic Syndrome',
        'short_name': 'AHUS',
        'features': [
            FEATURES.DIAGNOSES,
            FEATURES.COMORBIDITIES,
            FEATURES.RESULTS,
            FEATURES.MEDICATIONS,
            FEATURES.DIALYSIS,
            FEATURES.PLASMAPHERESIS,
            FEATURES.TRANSPLANTS,
        ],
        'result_group_codes': [],
    },
    {
        'code': 'CALCIP',
        'name': 'Calciphylaxis',
        'short_name': 'Calciphylaxis',
        'features': [
            FEATURES.DIAGNOSES,
            FEATURES.COMORBIDITIES,
            FEATURES.RESULTS,
        ],
        'result_group_codes': [],
    },
    {
        'code': 'CYSTIN',
        'name': 'Cystinosis',
        'short_name': 'Cystinosis',
        'features': [
            FEATURES.DIAGNOSES,
            FEATURES.MEDICATIONS,
            FEATURES.DIALYSIS,
            FEATURES.TRANSPLANTS,
            FEATURES.HOSPITALISATIONS,
        ],
        'result_group_codes': [],
    },
    {
        'code': 'CYSURIA',
        'name': 'Cystinuria',
        'short_name': 'Cystinuria',
        'features': [
            FEATURES.DIAGNOSES,
        ],
        'result_group_codes': [],
    },
    {
        'code': 'DENTLOWE',
        'name': 'Dent Disease and Lowe Syndrome',
        'short_name': 'Dent & Lowe',
        'features': [
            FEATURES.DIAGNOSES,
        ],
        'result_group_codes': [],
    },
    {
        'code': 'FUAN',
        'name': 'Familial Urate Associated Nephropathy',
        'short_name': 'FUAN',
        'features': [
            FEATURES.DIAGNOSES,
            FEATURES.GENETICS,
            FEATURES.RENAL_IMAGING,
            FEATURES.RESULTS,
            FEATURES.MEDICATIONS,
        ],
        'result_group_codes': [],
    },
    {
        'code': 'HNF1B',
        'name': 'HNF1b Mutations',
        'short_name': 'HNF1b',
        'features': [
            FEATURES.DIAGNOSES,
            FEATURES.FAMILY_HISTORY,
            FEATURES.RENAL_IMAGING,
            FEATURES.PATHOLOGY,
        ],
        'result_group_codes': [],
    },
    {
        'code': 'HYPERRDG',
        'name': 'Hyperoxaluria',
        'short_name': 'Hyperoxaluria',
        'features': [
            FEATURES.DIAGNOSES,
            FEATURES.GENETICS,
            FEATURES.RENAL_IMAGING,
            FEATURES.RESULTS,
            FEATURES.MEDICATIONS,
            FEATURES.DIALYSIS,
            FEATURES.TRANSPLANTS,
        ],
        'result_group_codes': [],
    },
    {
        'code': 'HYPALK',
        'name': 'Hypokalaemic Alkalosis',
        'short_name': 'Hypokalaemic Alkalosis',
        'features': [
            FEATURES.DIAGNOSES,
            FEATURES.COMORBIDITIES,
            FEATURES.RENAL_IMAGING,
            FEATURES.RESULTS,
            FEATURES.SALT_WASTING_CLINICAL_FEATURES,
            FEATURES.MEDICATIONS,
            FEATURES.DIALYSIS,
        ],
        'result_group_codes': [],
    },
    {
        'code': 'INS',
        'name': 'Idiopathic Nephrotic Syndrome',
        'short_name': 'INS',
        'features': [
            FEATURES.DIAGNOSES,
            FEATURES.GENETICS,
            FEATURES.FAMILY_HISTORY,
            FEATURES.COMORBIDITIES,
            FEATURES.PATHOLOGY,
            FEATURES.RESULTS,
            FEATURES.MEDICATIONS,
            FEATURES.DIALYSIS,
            FEATURES.PLASMAPHERESIS,
            FEATURES.TRANSPLANTS,
            FEATURES.HOSPITALISATIONS,
        ],
        'result_group_codes': [],
    },
    {
        'code': 'IGANEPHRO',
        'name': 'IgA Nephropathy',
        'short_name': 'IgA',
        'features': [
            FEATURES.DIAGNOSES,
        ],
        'result_group_codes': [],
    },
    {
        'code': 'MPGN',
        'name': 'Membranoproliferative Glomerulonephritis / Dense Deposit Disease',
        'short_name': 'MPGN',
        'features': [
            FEATURES.DIAGNOSES,
            FEATURES.GENETICS,
            FEATURES.FAMILY_HISTORY,
            FEATURES.COMORBIDITIES,
            FEATURES.PATHOLOGY,
            FEATURES.RESULTS,
            FEATURES.MEDICATIONS,
            FEATURES.DIALYSIS,
            FEATURES.TRANSPLANTS,
            FEATURES.HOSPITALISATIONS,
        ],
        'result_group_codes': [],
    },
    {
        'code': 'MEMRDG',
        'name': 'Membranous Nephropathy',
        'short_name': 'Membranous Nephropathy',
        'features': [
            FEATURES.DIAGNOSES,
        ],
        'result_group_codes': [],
    },
    {
        'code': 'NEPHROS',
        'name': 'NephroS',
        'short_name': 'NephroS',
        'features': [
            FEATURES.RESULTS,
        ],
        'result_group_codes': [],
    },
    {
        'code': 'OBS',
        'name': 'Pregnancy',
        'short_name': 'Pregnancy',
        'features': [
            FEATURES.DIAGNOSES,
            FEATURES.COMORBIDITIES,
            FEATURES.PATHOLOGY,
            FEATURES.RESULTS,
            FEATURES.MEDICATIONS,
            FEATURES.DIALYSIS,
            FEATURES.PLASMAPHERESIS,
            FEATURES.TRANSPLANTS,
            FEATURES.HOSPITALISATIONS,
        ],
        'result_group_codes': [],
    },
    {
        'code': 'PCRA',
        'name': 'Pure Red Cell Aplasia',
        'short_name': 'PCRA',
        'features': [
            FEATURES.DIAGNOSES,
        ],
        'result_group_codes': [],
    },
    {
        'code': 'STECHUS',
        'name': 'STEC-associated HUS',
        'short_name': 'STEC-HUS',
        'features': [
            FEATURES.DIAGNOSES,
            FEATURES.GENETICS,
            FEATURES.FAMILY_HISTORY,
            FEATURES.COMORBIDITIES,
            FEATURES.RESULTS,
            FEATURES.DIALYSIS,
            FEATURES.PLASMAPHERESIS,
            FEATURES.TRANSPLANTS,
        ],
        'result_group_codes': [],
    },
    {
        'code': 'VASRDG',
        'name': 'Vasculitis',
        'short_name': 'Vasculitis',
        'features': [
            FEATURES.DIAGNOSES,
            FEATURES.COMORBIDITIES,
            FEATURES.RENAL_IMAGING,
            FEATURES.PATHOLOGY,
            FEATURES.RESULTS,
            FEATURES.MEDICATIONS,
            FEATURES.TRANSPLANTS,
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
