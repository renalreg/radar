from sqlalchemy import create_engine, text
import click

from radar_migration import EXCLUDED_UNITS, Migration, tables


PHENOTYPE_MAP = {
    1: 'Autoimmune Disease',
    2: 'Mental Retardation Syndrome',
    3: 'Polydactyly',
    4: 'Blindness',
    5: 'Deafness',
    6: 'Cardiomyopathy',
    7: 'Congenital CMV',
    8: 'TORCH Syndrome',
    9: 'Diabetes',
    10: 'Microcephaly',
    11: 'Nail-Patella Syndrome',
    12: 'Cardiac Anomalies',
    13: 'Hepatitis B',
    14: 'Hepatitis C',
    15: 'CNS Abnormalitites',
    16: 'Spondyloepiphyseal Dysplasia',
    17: 'Microcoria',
    18: 'Male Pseudohermaphroditism',
}


def convert_phenotype(old_value):
    try:
        new_value = PHENOTYPE_MAP[old_value]
    except KeyError:
        raise ValueError('Unknown phenotype: %s' % old_value)

    return new_value


def migrate_phenotypes(old_conn, new_conn):
    m = Migration(new_conn)

    # Check all phenotypes exist
    for disorder_name in PHENOTYPE_MAP.values():
        m.get_disorder_id(disorder_name)

    rows = old_conn.execute(text("""
        SELECT
            x.radar_no,
            CASE
                WHEN from_date IS NOT NULL AND from_date != '0000-00-00 00:00:00' THEN
                    from_date
                ELSE
                    -- Use registration date if result date is missing
                    CAST(LEAST(
                        COALESCE(patient.dateReg, NOW()),
                        COALESCE(rdr_radar_number.creationDate, NOW()),
                        COALESCE(tbl_demographics.DATE_REG, NOW())
                    ) AS DATE)
            END as from_date,
            x.phenotype
        FROM (
            (
                SELECT
                    radar_no AS radar_no,
                    date_clin_pic AS from_date,
                    phenotype1 AS phenotype
                FROM tbl_clinicaldata
            )
            UNION
            (
                SELECT
                    radar_no AS radar_no,
                    date_clin_pic AS from_date,
                    phenotype2 AS phenotype
                FROM tbl_clinicaldata
            )
            UNION
            (
                SELECT
                    radar_no AS radar_no,
                    date_clin_pic AS from_date,
                    phenotype3 AS phenotype
                FROM tbl_clinicaldata
            )
            UNION
            (
                SELECT
                    radar_no AS radar_no,
                    date_clin_pic AS from_date,
                    phenotype4 AS phenotype
                FROM tbl_clinicaldata
            )
        ) AS x
        JOIN patient ON (
            x.radar_no = patient.radarNo AND
            patient.unitcode NOT IN {0}
        )
        LEFT JOIN rdr_radar_number ON patient.radarNo = rdr_radar_number.id
        LEFT JOIN tbl_demographics ON patient.radarNo = tbl_demographics.radar_no
        WHERE x.phenotype IS NOT NULL
    """.format(EXCLUDED_UNITS)))

    for row in rows:
        patient_id, from_date, phenotype = row
        diagnois_name = convert_phenotype(phenotype)
        diagnosis_id = m.get_diagnosis_id(diagnois_name)

        new_conn.execute(
            tables.patient_diagnoses.insert(),
            patient_id=patient_id,
            source_group_id=m.radar_group_id,
            source_type=m.radar_source_type,
            diagnosis_id=diagnosis_id,
            from_date=from_date,
            created_user_id=m.user_id,
            modified_user_id=m.user_id,
        )


@click.command()
@click.argument('src')
@click.argument('dest')
def cli(src, dest):
    src_engine = create_engine(src)
    dest_engine = create_engine(dest)

    src_conn = src_engine.connect()
    dest_conn = dest_engine.connect()

    with dest_conn.begin():
        migrate_phenotypes(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
