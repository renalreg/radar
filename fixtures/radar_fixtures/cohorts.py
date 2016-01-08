from radar_fixtures.validation import validate_and_add
from radar.models import Cohort, CohortFeature
from radar.features import FEATURES

COHORTS = [
    {
        'code': 'RADAR',
        'name': 'RaDaR',
        'short_name': 'RaDaR',
        'features': [
            FEATURES.DEMOGRAPHICS,
            FEATURES.CONSULTANTS,
            FEATURES.COHORTS,
            FEATURES.UNITS
        ],
    },
    {
        'code': 'ALPORT',
        'name': 'Alport Syndrome',
        'short_name': 'Alport',
        'features': [
            FEATURES.DIAGNOSIS,
            FEATURES.GENETICS,
            FEATURES.FAMILY_HISTORY,
            FEATURES.ALPORT_CLINICAL_PICTURES,
            FEATURES.RESULTS,
        ],
    },
    {
        'code': 'APRT',
        'name': 'APRT Deficiency',
        'short_name': 'APRT',
        'features': [
            FEATURES.DIAGNOSIS,
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
    },
    {
        'code': 'ARPKD',
        'name': 'Autosomal Recessive Polycystic Kidney Disease',
        'short_name': 'ARPKD',
        'features': [
            FEATURES.DIAGNOSIS,
            FEATURES.COMORBIDITIES,
            FEATURES.RENAL_IMAGING,
            FEATURES.PATHOLOGY,
            FEATURES.RESULTS,
            FEATURES.MEDICATIONS,
            FEATURES.DIALYSIS,
            FEATURES.TRANSPLANTS,
        ],
    },
    {
        'code': 'AHUS',
        'name': 'Atypical Haemolytic Uraemic Syndrome',
        'short_name': 'AHUS',
        'features': [
            FEATURES.DIAGNOSIS,
            FEATURES.COMORBIDITIES,
            FEATURES.RESULTS,
            FEATURES.MEDICATIONS,
            FEATURES.DIALYSIS,
            FEATURES.PLASMAPHERESIS,
            FEATURES.TRANSPLANTS,
        ],
    },
    {
        'code': 'CALCIP',
        'name': 'Calciphylaxis',
        'short_name': 'Calciphylaxis',
        'features': [
            FEATURES.DIAGNOSIS,
            FEATURES.COMORBIDITIES,
            FEATURES.RESULTS,
        ],
    },
    {
        'code': 'CYSTIN',
        'name': 'Cystinosis',
        'short_name': 'Cystinosis',
        'features': [
            FEATURES.DIAGNOSIS,
            FEATURES.MEDICATIONS,
            FEATURES.DIALYSIS,
            FEATURES.TRANSPLANTS,
            FEATURES.HOSPITALISATIONS,
        ],
    },
    {
        'code': 'CYSURIA',
        'name': 'Cystinuria',
        'short_name': 'Cystinuria',
        'features': [
            FEATURES.DIAGNOSIS,
        ],
    },
    {
        'code': 'DENTLOWE',
        'name': 'Dent Disease and Lowe Syndrome',
        'short_name': 'Dent & Lowe',
        'features': [
            FEATURES.DIAGNOSIS,
        ],
    },
    {
        'code': 'FUAN',
        'name': 'Familial Urate Associated Nephropathy',
        'short_name': 'FUAN',
        'features': [
            FEATURES.DIAGNOSIS,
            FEATURES.GENETICS,
            FEATURES.RENAL_IMAGING,
            FEATURES.RESULTS,
            FEATURES.MEDICATIONS,
        ],
    },
    {
        'code': 'HNF1B',
        'name': 'HNF1b Mutations',
        'short_name': 'HNF1b',
        'features': [
            FEATURES.DIAGNOSIS,
            FEATURES.FAMILY_HISTORY,
            FEATURES.RENAL_IMAGING,
            FEATURES.PATHOLOGY,
        ],
    },
    {
        'code': 'HYPOXAL',
        'name': 'Hyperoxaluria',
        'short_name': 'Hyperoxaluria',
        'features': [
            FEATURES.DIAGNOSIS,
            FEATURES.GENETICS,
            FEATURES.RENAL_IMAGING,
            FEATURES.RESULTS,
            FEATURES.MEDICATIONS,
            FEATURES.DIALYSIS,
            FEATURES.TRANSPLANTS,
        ],
    },
    {
        'code': 'HYPALK',
        'name': 'Hypokalaemic Alkalosis',
        'short_name': 'Hypokalaemic Alkalosis',
        'features': [
            FEATURES.DIAGNOSIS,
            FEATURES.GENETICS,
            FEATURES.SALT_WASTING_CLINICAL_FEATURES,
            FEATURES.COMORBIDITIES,
            FEATURES.RENAL_IMAGING,
            FEATURES.RESULTS,
            FEATURES.MEDICATIONS,
            FEATURES.DIALYSIS,
        ],
    },
    {
        'code': 'INS',
        'name': 'Idiopathic Nephrotic Syndrome',
        'short_name': 'INS',
        'features': [
            FEATURES.DIAGNOSIS,
            FEATURES.GENETICS,
            FEATURES.FAMILY_HISTORY,
            FEATURES.COMORBIDITIES,
            FEATURES.PATHOLOGY,
            FEATURES.INS_CLINICAL_PICTURES,
            FEATURES.RESULTS,
            FEATURES.MEDICATIONS,
            FEATURES.INS_RELAPSES,
            FEATURES.DIALYSIS,
            FEATURES.PLASMAPHERESIS,
            FEATURES.TRANSPLANTS,
            FEATURES.HOSPITALISATIONS,
        ],
    },
    {
        'code': 'IGANEPHRO',
        'name': 'IgA Nephropathy',
        'short_name': 'IgA',
        'features': [
            FEATURES.DIAGNOSIS,
        ],
    },
    {
        'code': 'MPGN',
        'name': 'Membranoproliferative Glomerulonephritis / Dense Deposit Disease',
        'short_name': 'MPGN',
        'features': [
            FEATURES.DIAGNOSIS,
            FEATURES.MPGN_CLINICAL_PICTURES,
            FEATURES.PATHOLOGY,
            FEATURES.RESULTS,
            FEATURES.MEDICATIONS,
            FEATURES.DIALYSIS,
            FEATURES.PLASMAPHERESIS,
            FEATURES.TRANSPLANTS,
        ],
    },
    {
        'code': 'MEMNEPHRO',
        'name': 'Membranous Nephropathy',
        'short_name': 'Membranous Nephropathy',
        'features': [
            FEATURES.DIAGNOSIS,
        ],
    },
    {
        'code': 'NEPHROS',
        'name': 'NephroS',
        'short_name': 'NephroS',
        'features': [
            FEATURES.RESULTS,
        ],
    },
    {
        'code': 'NSMPGNC3',
        'name': 'National Study of Membranoproliferative Glomerulonephritis (MPGN) and C3 Glomerulopathy (C3G)',
        'short_name': 'National Study of MPGN and C3',
        'features': [
            FEATURES.RESULTS,
        ],
    },
    {
        'code': 'OBS',
        'name': 'Pregnancy',
        'short_name': 'Pregnancy',
        'features': [
            FEATURES.DIAGNOSIS,
            FEATURES.PREGNANCIES,
            FEATURES.FETAL_ULTRASOUNDS,
            FEATURES.RESULTS,
            FEATURES.MEDICATIONS,
            FEATURES.DIALYSIS,
            FEATURES.TRANSPLANTS,
        ],
    },
    {
        'code': 'PRCA',
        'name': 'Pure Red Cell Aplasia',
        'short_name': 'PRCA',
        'features': [
            FEATURES.DIAGNOSIS,
        ],
    },
    {
        'code': 'STECHUS',
        'name': 'STEC-associated HUS',
        'short_name': 'STEC-HUS',
        'features': [
            FEATURES.DIAGNOSIS,
            FEATURES.GENETICS,
            FEATURES.FAMILY_HISTORY,
            FEATURES.COMORBIDITIES,
            FEATURES.RESULTS,
            FEATURES.DIALYSIS,
            FEATURES.PLASMAPHERESIS,
            FEATURES.TRANSPLANTS,
        ],
    },
    {
        'code': 'VAS',
        'name': 'Vasculitis',
        'short_name': 'Vasculitis',
        'features': [
            FEATURES.DIAGNOSIS,
            FEATURES.COMORBIDITIES,
            FEATURES.RENAL_IMAGING,
            FEATURES.PATHOLOGY,
            FEATURES.RESULTS,
            FEATURES.MEDICATIONS,
            FEATURES.TRANSPLANTS,
        ],
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
            cohort_feature.display_order = i
            validate_and_add(cohort_feature)
