from radar_fixtures.validation import validate_and_add
from radar.models.groups import Group, GROUP_TYPE_COHORT
from radar.pages import PAGE

COHORTS = [
    {
        'code': 'ALPORT',
        'name': 'Alport Syndrome',
        'short_name': 'Alport',
        'pages': [
            PAGE.DIAGNOSIS,
            PAGE.GENETICS,
            PAGE.FAMILY_HISTORY,
            PAGE.ALPORT_CLINICAL_PICTURES,
            PAGE.RESULTS,
        ],
    },
    {
        'code': 'APRT',
        'name': 'APRT Deficiency',
        'short_name': 'APRT',
        'pages': [
            PAGE.DIAGNOSIS,
            PAGE.GENETICS,
            PAGE.FAMILY_HISTORY,
            PAGE.COMORBIDITIES,
            PAGE.RENAL_IMAGING,
            PAGE.PATHOLOGY,
            PAGE.RESULTS,
            PAGE.MEDICATIONS,
            PAGE.DIALYSIS,
            PAGE.TRANSPLANTS,
        ],
    },
    {
        'code': 'ARPKD',
        'name': 'Autosomal Recessive Polycystic Kidney Disease',
        'short_name': 'ARPKD',
        'pages': [
            PAGE.DIAGNOSIS,
            PAGE.COMORBIDITIES,
            PAGE.RENAL_IMAGING,
            PAGE.PATHOLOGY,
            PAGE.RESULTS,
            PAGE.MEDICATIONS,
            PAGE.DIALYSIS,
            PAGE.TRANSPLANTS,
        ],
    },
    {
        'code': 'AHUS',
        'name': 'Atypical Haemolytic Uraemic Syndrome',
        'short_name': 'AHUS',
        'pages': [
            PAGE.DIAGNOSIS,
            PAGE.COMORBIDITIES,
            PAGE.RESULTS,
            PAGE.MEDICATIONS,
            PAGE.DIALYSIS,
            PAGE.PLASMAPHERESIS,
            PAGE.TRANSPLANTS,
        ],
    },
    {
        'code': 'CALCIP',
        'name': 'Calciphylaxis',
        'short_name': 'Calciphylaxis',
        'pages': [
            PAGE.DIAGNOSIS,
            PAGE.COMORBIDITIES,
            PAGE.RESULTS,
        ],
    },
    {
        'code': 'CYSTIN',
        'name': 'Cystinosis',
        'short_name': 'Cystinosis',
        'pages': [
            PAGE.DIAGNOSIS,
            PAGE.MEDICATIONS,
            PAGE.DIALYSIS,
            PAGE.TRANSPLANTS,
            PAGE.HOSPITALISATIONS,
        ],
    },
    {
        'code': 'CYSURIA',
        'name': 'Cystinuria',
        'short_name': 'Cystinuria',
        'pages': [
            PAGE.DIAGNOSIS,
        ],
    },
    {
        'code': 'DENTLOWE',
        'name': 'Dent Disease and Lowe Syndrome',
        'short_name': 'Dent & Lowe',
        'pages': [
            PAGE.DIAGNOSIS,
        ],
    },
    {
        'code': 'FUAN',
        'name': 'Familial Urate Associated Nephropathy',
        'short_name': 'FUAN',
        'pages': [
            PAGE.DIAGNOSIS,
            PAGE.GENETICS,
            PAGE.RENAL_IMAGING,
            PAGE.RESULTS,
            PAGE.MEDICATIONS,
        ],
    },
    {
        'code': 'HNF1B',
        'name': 'HNF1b Mutations',
        'short_name': 'HNF1b',
        'pages': [
            PAGE.DIAGNOSIS,
            PAGE.FAMILY_HISTORY,
            PAGE.RENAL_IMAGING,
            PAGE.PATHOLOGY,
        ],
    },
    {
        'code': 'HYPOXAL',
        'name': 'Hyperoxaluria',
        'short_name': 'Hyperoxaluria',
        'pages': [
            PAGE.DIAGNOSIS,
            PAGE.GENETICS,
            PAGE.RENAL_IMAGING,
            PAGE.RESULTS,
            PAGE.MEDICATIONS,
            PAGE.DIALYSIS,
            PAGE.TRANSPLANTS,
        ],
    },
    {
        'code': 'HYPALK',
        'name': 'Hypokalaemic Alkalosis',
        'short_name': 'Hypokalaemic Alkalosis',
        'pages': [
            PAGE.DIAGNOSIS,
            PAGE.GENETICS,
            PAGE.SALT_WASTING_CLINICAL_FEATURES,
            PAGE.COMORBIDITIES,
            PAGE.RENAL_IMAGING,
            PAGE.RESULTS,
            PAGE.MEDICATIONS,
            PAGE.DIALYSIS,
        ],
    },
    {
        'code': 'INS',
        'name': 'Idiopathic Nephrotic Syndrome',
        'short_name': 'INS',
        'pages': [
            PAGE.DIAGNOSIS,
            PAGE.GENETICS,
            PAGE.FAMILY_HISTORY,
            PAGE.COMORBIDITIES,
            PAGE.PATHOLOGY,
            PAGE.INS_CLINICAL_PICTURES,
            PAGE.RESULTS,
            PAGE.MEDICATIONS,
            PAGE.INS_RELAPSES,
            PAGE.DIALYSIS,
            PAGE.PLASMAPHERESIS,
            PAGE.TRANSPLANTS,
            PAGE.HOSPITALISATIONS,
        ],
    },
    {
        'code': 'IGANEPHRO',
        'name': 'IgA Nephropathy',
        'short_name': 'IgA',
        'pages': [
            PAGE.DIAGNOSIS,
        ],
    },
    {
        'code': 'MPGN',
        'name': 'Membranoproliferative Glomerulonephritis / Dense Deposit Disease',
        'short_name': 'MPGN',
        'pages': [
            PAGE.DIAGNOSIS,
            PAGE.MPGN_CLINICAL_PICTURES,
            PAGE.PATHOLOGY,
            PAGE.RESULTS,
            PAGE.MEDICATIONS,
            PAGE.DIALYSIS,
            PAGE.PLASMAPHERESIS,
            PAGE.TRANSPLANTS,
        ],
    },
    {
        'code': 'MEMNEPHRO',
        'name': 'Membranous Nephropathy',
        'short_name': 'Membranous Nephropathy',
        'pages': [
            PAGE.DIAGNOSIS,
        ],
    },
    {
        'code': 'NEPHROS',
        'name': 'NephroS',
        'short_name': 'NephroS',
        'pages': [
            PAGE.RESULTS,
        ],
    },
    {
        'code': 'NSMPGNC3',
        'name': 'National Study of Membranoproliferative Glomerulonephritis (MPGN) and C3 Glomerulopathy (C3G)',
        'short_name': 'National Study of MPGN and C3',
        'pages': [
            PAGE.RESULTS,
        ],
    },
    {
        'code': 'OBS',
        'name': 'Pregnancy',
        'short_name': 'Pregnancy',
        'pages': [
            PAGE.DIAGNOSIS,
            PAGE.PREGNANCIES,
            PAGE.FETAL_ULTRASOUNDS,
            PAGE.RESULTS,
            PAGE.MEDICATIONS,
            PAGE.DIALYSIS,
            PAGE.TRANSPLANTS,
        ],
    },
    {
        'code': 'PRCA',
        'name': 'Pure Red Cell Aplasia',
        'short_name': 'PRCA',
        'pages': [
            PAGE.DIAGNOSIS,
        ],
    },
    {
        'code': 'STECHUS',
        'name': 'STEC-associated HUS',
        'short_name': 'STEC-HUS',
        'pages': [
            PAGE.DIAGNOSIS,
            PAGE.GENETICS,
            PAGE.FAMILY_HISTORY,
            PAGE.COMORBIDITIES,
            PAGE.RESULTS,
            PAGE.DIALYSIS,
            PAGE.PLASMAPHERESIS,
            PAGE.TRANSPLANTS,
        ],
    },
    {
        'code': 'VAS',
        'name': 'Vasculitis',
        'short_name': 'Vasculitis',
        'pages': [
            PAGE.DIAGNOSIS,
            PAGE.COMORBIDITIES,
            PAGE.RENAL_IMAGING,
            PAGE.PATHOLOGY,
            PAGE.RESULTS,
            PAGE.MEDICATIONS,
            PAGE.TRANSPLANTS,
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
