from radar_fixtures.validation import validate_and_add
from radar.models.groups import Group, GROUP_TYPE_COHORT
from radar.pages import PAGES

COHORTS = [
    {
        'code': 'RADAR',
        'name': 'RaDaR',
        'short_name': 'RaDaR',
        'pages': [
            PAGES.DEMOGRAPHICS,
            PAGES.CONSULTANTS,
            PAGES.COHORTS,
            PAGES.UNITS
        ],
    },
    {
        'code': 'ALPORT',
        'name': 'Alport Syndrome',
        'short_name': 'Alport',
        'pages': [
            PAGES.DIAGNOSIS,
            PAGES.GENETICS,
            PAGES.FAMILY_HISTORY,
            PAGES.ALPORT_CLINICAL_PICTURES,
            PAGES.RESULTS,
        ],
    },
    {
        'code': 'APRT',
        'name': 'APRT Deficiency',
        'short_name': 'APRT',
        'pages': [
            PAGES.DIAGNOSIS,
            PAGES.GENETICS,
            PAGES.FAMILY_HISTORY,
            PAGES.COMORBIDITIES,
            PAGES.RENAL_IMAGING,
            PAGES.PATHOLOGY,
            PAGES.RESULTS,
            PAGES.MEDICATIONS,
            PAGES.DIALYSIS,
            PAGES.TRANSPLANTS,
        ],
    },
    {
        'code': 'ARPKD',
        'name': 'Autosomal Recessive Polycystic Kidney Disease',
        'short_name': 'ARPKD',
        'pages': [
            PAGES.DIAGNOSIS,
            PAGES.COMORBIDITIES,
            PAGES.RENAL_IMAGING,
            PAGES.PATHOLOGY,
            PAGES.RESULTS,
            PAGES.MEDICATIONS,
            PAGES.DIALYSIS,
            PAGES.TRANSPLANTS,
        ],
    },
    {
        'code': 'AHUS',
        'name': 'Atypical Haemolytic Uraemic Syndrome',
        'short_name': 'AHUS',
        'pages': [
            PAGES.DIAGNOSIS,
            PAGES.COMORBIDITIES,
            PAGES.RESULTS,
            PAGES.MEDICATIONS,
            PAGES.DIALYSIS,
            PAGES.PLASMAPHERESIS,
            PAGES.TRANSPLANTS,
        ],
    },
    {
        'code': 'CALCIP',
        'name': 'Calciphylaxis',
        'short_name': 'Calciphylaxis',
        'pages': [
            PAGES.DIAGNOSIS,
            PAGES.COMORBIDITIES,
            PAGES.RESULTS,
        ],
    },
    {
        'code': 'CYSTIN',
        'name': 'Cystinosis',
        'short_name': 'Cystinosis',
        'pages': [
            PAGES.DIAGNOSIS,
            PAGES.MEDICATIONS,
            PAGES.DIALYSIS,
            PAGES.TRANSPLANTS,
            PAGES.HOSPITALISATIONS,
        ],
    },
    {
        'code': 'CYSURIA',
        'name': 'Cystinuria',
        'short_name': 'Cystinuria',
        'pages': [
            PAGES.DIAGNOSIS,
        ],
    },
    {
        'code': 'DENTLOWE',
        'name': 'Dent Disease and Lowe Syndrome',
        'short_name': 'Dent & Lowe',
        'pages': [
            PAGES.DIAGNOSIS,
        ],
    },
    {
        'code': 'FUAN',
        'name': 'Familial Urate Associated Nephropathy',
        'short_name': 'FUAN',
        'pages': [
            PAGES.DIAGNOSIS,
            PAGES.GENETICS,
            PAGES.RENAL_IMAGING,
            PAGES.RESULTS,
            PAGES.MEDICATIONS,
        ],
    },
    {
        'code': 'HNF1B',
        'name': 'HNF1b Mutations',
        'short_name': 'HNF1b',
        'pages': [
            PAGES.DIAGNOSIS,
            PAGES.FAMILY_HISTORY,
            PAGES.RENAL_IMAGING,
            PAGES.PATHOLOGY,
        ],
    },
    {
        'code': 'HYPOXAL',
        'name': 'Hyperoxaluria',
        'short_name': 'Hyperoxaluria',
        'pages': [
            PAGES.DIAGNOSIS,
            PAGES.GENETICS,
            PAGES.RENAL_IMAGING,
            PAGES.RESULTS,
            PAGES.MEDICATIONS,
            PAGES.DIALYSIS,
            PAGES.TRANSPLANTS,
        ],
    },
    {
        'code': 'HYPALK',
        'name': 'Hypokalaemic Alkalosis',
        'short_name': 'Hypokalaemic Alkalosis',
        'pages': [
            PAGES.DIAGNOSIS,
            PAGES.GENETICS,
            PAGES.SALT_WASTING_CLINICAL_FEATURES,
            PAGES.COMORBIDITIES,
            PAGES.RENAL_IMAGING,
            PAGES.RESULTS,
            PAGES.MEDICATIONS,
            PAGES.DIALYSIS,
        ],
    },
    {
        'code': 'INS',
        'name': 'Idiopathic Nephrotic Syndrome',
        'short_name': 'INS',
        'pages': [
            PAGES.DIAGNOSIS,
            PAGES.GENETICS,
            PAGES.FAMILY_HISTORY,
            PAGES.COMORBIDITIES,
            PAGES.PATHOLOGY,
            PAGES.INS_CLINICAL_PICTURES,
            PAGES.RESULTS,
            PAGES.MEDICATIONS,
            PAGES.INS_RELAPSES,
            PAGES.DIALYSIS,
            PAGES.PLASMAPHERESIS,
            PAGES.TRANSPLANTS,
            PAGES.HOSPITALISATIONS,
        ],
    },
    {
        'code': 'IGANEPHRO',
        'name': 'IgA Nephropathy',
        'short_name': 'IgA',
        'pages': [
            PAGES.DIAGNOSIS,
        ],
    },
    {
        'code': 'MPGN',
        'name': 'Membranoproliferative Glomerulonephritis / Dense Deposit Disease',
        'short_name': 'MPGN',
        'pages': [
            PAGES.DIAGNOSIS,
            PAGES.MPGN_CLINICAL_PICTURES,
            PAGES.PATHOLOGY,
            PAGES.RESULTS,
            PAGES.MEDICATIONS,
            PAGES.DIALYSIS,
            PAGES.PLASMAPHERESIS,
            PAGES.TRANSPLANTS,
        ],
    },
    {
        'code': 'MEMNEPHRO',
        'name': 'Membranous Nephropathy',
        'short_name': 'Membranous Nephropathy',
        'pages': [
            PAGES.DIAGNOSIS,
        ],
    },
    {
        'code': 'NEPHROS',
        'name': 'NephroS',
        'short_name': 'NephroS',
        'pages': [
            PAGES.RESULTS,
        ],
    },
    {
        'code': 'NSMPGNC3',
        'name': 'National Study of Membranoproliferative Glomerulonephritis (MPGN) and C3 Glomerulopathy (C3G)',
        'short_name': 'National Study of MPGN and C3',
        'pages': [
            PAGES.RESULTS,
        ],
    },
    {
        'code': 'OBS',
        'name': 'Pregnancy',
        'short_name': 'Pregnancy',
        'pages': [
            PAGES.DIAGNOSIS,
            PAGES.PREGNANCIES,
            PAGES.FETAL_ULTRASOUNDS,
            PAGES.RESULTS,
            PAGES.MEDICATIONS,
            PAGES.DIALYSIS,
            PAGES.TRANSPLANTS,
        ],
    },
    {
        'code': 'PRCA',
        'name': 'Pure Red Cell Aplasia',
        'short_name': 'PRCA',
        'pages': [
            PAGES.DIAGNOSIS,
        ],
    },
    {
        'code': 'STECHUS',
        'name': 'STEC-associated HUS',
        'short_name': 'STEC-HUS',
        'pages': [
            PAGES.DIAGNOSIS,
            PAGES.GENETICS,
            PAGES.FAMILY_HISTORY,
            PAGES.COMORBIDITIES,
            PAGES.RESULTS,
            PAGES.DIALYSIS,
            PAGES.PLASMAPHERESIS,
            PAGES.TRANSPLANTS,
        ],
    },
    {
        'code': 'VAS',
        'name': 'Vasculitis',
        'short_name': 'Vasculitis',
        'pages': [
            PAGES.DIAGNOSIS,
            PAGES.COMORBIDITIES,
            PAGES.RENAL_IMAGING,
            PAGES.PATHOLOGY,
            PAGES.RESULTS,
            PAGES.MEDICATIONS,
            PAGES.TRANSPLANTS,
        ],
    },
]


def create_cohorts():
    for x in COHORTS:
        group = Group()
        group.type = GROUP_TYPE_COHORT
        group.code = x['code']
        group.name = x['name']
        group.short_name = x['short_name']
        group.pages = x['pages']
        group = validate_and_add(group)
