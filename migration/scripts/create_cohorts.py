import csv
from collections import defaultdict

import click
from sqlalchemy import create_engine

from radar_migration import tables, Migration
from radar_migration.cohorts import create_cohort


COHORTS = [
    {
        'code': 'ALPORT',
        'name': 'Alport Syndrome',
        'short_name': 'Alport',
        'features': [
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
        'features': [
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
        'code': 'ARPKD',
        'name': 'Autosomal Recessive Polycystic Kidney Disease',
        'short_name': 'ARPKD',
        'features': [
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
        'features': [
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
        'features': [
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
        'features': [
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
        'features': [
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
        'features': [
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
        'features': [
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
        'features': [
            'DIAGNOSIS',
            'GENETICS',
            'FAMILY_HISTORY',
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
        'features': [
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
        'features': [
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
        'features': [
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
        'features': [
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
        'features': [
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
        'features': [
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
        'features': [],
    },
    {
        'code': 'NSMPGNC3',
        'name': 'National Study of Membranoproliferative Glomerulonephritis (MPGN) and C3 Glomerulopathy (C3G)',
        'short_name': 'National Study of MPGN and C3',
        'features': [],
    },
    {
        'code': 'OBS',
        'name': 'Pregnancy',
        'short_name': 'Pregnancy',
        'features': [
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
        'features': [
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
        'features': [
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
        'features': [
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
    for x in COHORTS:
        create_cohort(conn, x)


def create_cohort_diagnoses(conn, filename):
    m = Migration(conn)

    with open(filename, 'rb') as f:
        reader = csv.reader(f)

        cohort_diagnoses = defaultdict(list)

        for row in reader:
            cohort_diagnoses[row[0]].append(row[1])

        for code, diagnoses in cohort_diagnoses.items():
            cohort_id = m.get_cohort_id(code)
            i = 0

            for diagnosis in diagnoses:
                # Leave gaps between diagnoses
                display_order = 1000 + i * 100

                conn.execute(
                    tables.cohort_diagnoses.insert(),
                    cohort_id=cohort_id,
                    name=diagnosis,
                    display_order=display_order,
                )

                i += 1

    # TODO check all cohorts have diagnoses


@click.command()
@click.argument('db')
@click.argument('cohort_diagnoses')
def cli(db, cohort_diagnoses):
    engine = create_engine(db)
    conn = engine.connect()

    with conn.begin():
        create_cohorts(conn)
        create_cohort_diagnoses(conn, cohort_diagnoses)


if __name__ == '__main__':
    cli()
