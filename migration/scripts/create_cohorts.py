import copy

import click
from sqlalchemy import create_engine

from radar_migration.groups import create_group


COHORTS = [
    {
        'code': 'ALPORT',
        'name': 'Alport Syndrome',
        'short_name': 'Alport',
        'pages': [
            'DIAGNOSIS',
            'GENETICS',
            'FAMILY_HISTORY',
            'ALPORT_CLINICAL_PICTURES',
            'RESULTS',
        ],
    },
    {
        'code': 'APRT',
        'name': 'APRT Deficiency',
        'short_name': 'APRT',
        'pages': [
            'DIAGNOSIS',
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
    },
    {
        'code': 'ADPKD',
        'name': 'Autosomal Dominant Polycystic Kidney Disease',
        'short_name': 'ADPKD',
        'pages': [
            'DIAGNOSIS',
            'COMORBIDITIES',
            'RENAL_IMAGING',
            'PATHOLOGY',
            'RESULTS',
            'MEDICATIONS',
            'DIALYSIS',
            'TRANSPLANTS',
            'NEPHRECTOMIES',
        ],
    },
    {
        'code': 'ARPKD',
        'name': 'Autosomal Recessive Polycystic Kidney Disease',
        'short_name': 'ARPKD',
        'pages': [
            'DIAGNOSIS',
            'COMORBIDITIES',
            'RENAL_IMAGING',
            'PATHOLOGY',
            'RESULTS',
            'MEDICATIONS',
            'DIALYSIS',
            'TRANSPLANTS',
        ],
    },
    {
        'code': 'AHUS',
        'name': 'Atypical Haemolytic Uraemic Syndrome',
        'short_name': 'AHUS',
        'pages': [
            'DIAGNOSIS',
            'COMORBIDITIES',
            'RESULTS',
            'MEDICATIONS',
            'DIALYSIS',
            'PLASMAPHERESIS',
            'TRANSPLANTS',
        ],
    },
    {
        'code': 'CALCIP',
        'name': 'Calciphylaxis',
        'short_name': 'Calciphylaxis',
        'pages': [
            'DIAGNOSIS',
            'COMORBIDITIES',
            'RESULTS',
            'RENAL_IMAGING',
        ],
    },
    {
        'code': 'CYSTIN',
        'name': 'Cystinosis',
        'short_name': 'Cystinosis',
        'pages': [
            'DIAGNOSIS',
            'GENETICS',
            'RENAL_IMAGING',
            'RESULTS',
            'MEDICATIONS',
            'DIALYSIS',
            'TRANSPLANTS',
        ],
    },
    {
        'code': 'CYSURIA',
        'name': 'Cystinuria',
        'short_name': 'Cystinuria',
        'pages': [
            'DIAGNOSIS',
            'GENETICS',
            'RENAL_IMAGING',
            'RESULTS',
        ],
    },
    {
        'code': 'DENTLOWE',
        'name': 'Dent Disease and Lowe Syndrome',
        'short_name': 'Dent & Lowe',
        'pages': [
            'DIAGNOSIS',
            'GENETICS',
            'RENAL_IMAGING',
            'RESULTS',
        ],
    },
    {
        'code': 'FUAN',
        'name': 'Familial Urate Associated Nephropathy',
        'short_name': 'FUAN',
        'pages': [
            'DIAGNOSIS',
            'GENETICS',
            'RENAL_IMAGING',
            'RESULTS',
            'MEDICATIONS',
            'DIALYSIS',
            'TRANSPLANTS',
        ],
    },
    {
        'code': 'HNF1B',
        'name': 'HNF1b Mutations',
        'short_name': 'HNF1b',
        'pages': [
            'DIAGNOSIS',
            'GENETICS',
            'FAMILY_HISTORY',
            'FETAL_ANOMALY_SCANS',
            'RENAL_IMAGING',
            'PATHOLOGY',
            'RESULTS',
            'MEDICATIONS',
            'DIALYSIS',
        ],
    },
    {
        'code': 'HYPOXAL',
        'name': 'Hyperoxaluria',
        'short_name': 'Hyperoxaluria',
        'pages': [
            'DIAGNOSIS',
            'GENETICS',
            'RENAL_IMAGING',
            'RESULTS',
            'MEDICATIONS',
            'DIALYSIS',
            'TRANSPLANTS',
        ],
    },
    {
        'code': 'HYPALK',
        'name': 'Hypokalaemic Alkalosis',
        'short_name': 'Hypokalaemic Alkalosis',
        'pages': [
            'DIAGNOSIS',
            'GENETICS',
            'SALT_WASTING_CLINICAL_FEATURES',
            'COMORBIDITIES',
            'RENAL_IMAGING',
            'RESULTS',
            'MEDICATIONS',
            'DIALYSIS',
        ],
    },
    {
        'code': 'INS',
        'name': 'Idiopathic Nephrotic Syndrome',
        'short_name': 'INS',
        'pages': [
            'DIAGNOSIS',
            'GENETICS',
            'FAMILY_HISTORY',
            'COMORBIDITIES',
            'PATHOLOGY',
            'INS_CLINICAL_PICTURES',
            'RESULTS',
            'MEDICATIONS',
            'INS_RELAPSES',
            'DIALYSIS',
            'PLASMAPHERESIS',
            'TRANSPLANTS',
            'HOSPITALISATIONS',
        ],
    },
    {
        'code': 'IGANEPHRO',
        'name': 'IgA Nephropathy',
        'short_name': 'IgA',
        'pages': [
            'DIAGNOSIS',
            'GENETICS',
            'RESULTS',
            'MEDICATIONS',
            'DIALYSIS',
            'TRANSPLANTS',
        ],
    },
    {
        'code': 'MPGN',
        'name': 'Membranoproliferative Glomerulonephritis / Dense Deposit Disease',
        'short_name': 'MPGN',
        'pages': [
            'DIAGNOSIS',
            'GENETICS',
            'FAMILY_HISTORY',
            'COMORBIDITIES',
            'PATHOLOGY',
            'MPGN_CLINICAL_PICTURES',
            'RESULTS',
            'MEDICATIONS',
            'DIALYSIS',
            'PLASMAPHERESIS',
            'TRANSPLANTS',
            'HOSPITALISATIONS',
        ],
    },
    {
        'code': 'MEMNEPHRO',
        'name': 'Membranous Nephropathy',
        'short_name': 'Membranous Nephropathy',
        'pages': [
            'DIAGNOSIS',
            'GENETICS',
            'RESULTS',
            'MEDICATIONS',
            'DIALYSIS',
            'TRANSPLANTS',
        ],
    },
    {
        'code': 'NEPHROS',
        'name': 'NephroS',
        'short_name': 'NephroS',
        'pages': [],
    },
    {
        'code': 'NSMPGNC3',
        'name': 'National Study of Membranoproliferative Glomerulonephritis (MPGN) and C3 Glomerulopathy (C3G)',
        'short_name': 'National Study of MPGN and C3',
        'pages': [],
    },
    {
        'code': 'OBS',
        'name': 'Pregnancy',
        'short_name': 'Pregnancy',
        'pages': [
            'DIAGNOSIS',
            'PREGNANCIES',
            'FETAL_ULTRASOUNDS',
            'RESULTS',
            'MEDICATIONS',
            'DIALYSIS',
            'TRANSPLANTS',
        ],
    },
    {
        'code': 'PRCA',
        'name': 'Pure Red Cell Aplasia',
        'short_name': 'PRCA',
        'pages': [
            'DIAGNOSIS',
            'GENETICS',
            'RESULTS',
            'MEDICATIONS',
        ],
    },
    {
        'code': 'STECHUS',
        'name': 'STEC-associated HUS',
        'short_name': 'STEC HUS',
        'pages': [
            'DIAGNOSIS',
            'GENETICS',
            'FAMILY_HISTORY',
            'COMORBIDITIES',
            'RESULTS',
            'DIALYSIS',
            'PLASMAPHERESIS',
            'TRANSPLANTS',
        ],
    },
    {
        'code': 'VAS',
        'name': 'Vasculitis',
        'short_name': 'Vasculitis',
        'pages': [
            'DIAGNOSIS',
            'COMORBIDITIES',
            'RENAL_IMAGING',
            'PATHOLOGY',
            'RESULTS',
            'MEDICATIONS',
            'DIALYSIS',
            'TRANSPLANTS',
        ],
    },
]


def create_cohorts(conn):
    for cohort in COHORTS:
        cohort = copy.deepcopy(cohort)
        cohort['type'] = 'COHORT'
        create_group(conn, cohort)


@click.command()
@click.argument('db')
def cli(db):
    engine = create_engine(db)
    conn = engine.connect()

    with conn.begin():
        create_cohorts(conn)


if __name__ == '__main__':
    cli()
