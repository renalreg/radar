from sqlalchemy import create_engine, text
import click

from radar_migration import Migration, tables, EXCLUDED_UNITS


def migrate_diagnoses(old_conn, new_conn):
    m = Migration(new_conn)

    q = """
        SELECT
            x.radar_no,
            CASE
                WHEN x.from_date IS NOT NULL THEN
                    x.from_date
                ELSE
                    -- Use registration date if from date is missing
                    CAST(LEAST(
                        COALESCE(patient.dateReg, NOW()),
                        COALESCE(rdr_radar_number.creationDate, NOW()),
                        COALESCE(tbl_demographics.DATE_REG, NOW())
                    ) AS DATE)
            END as from_date,
            x.diagnosis_name
        FROM (
            (
                SELECT
                    radar_no as radar_no,
                    dateAtDiabetesDiagnosis as from_date,
                    'Diabetes' as diagnosis_name
                FROM rdr_hnf1b_misc
                WHERE diabetes = 1
            )
            UNION
            (
                SELECT
                    radar_no,
                    dateAtGoutDiagnosis,
                    'Gout'
                FROM rdr_hnf1b_misc
                WHERE gout = 1
            )
            UNION
            (
                SELECT
                    radar_no,
                    date_clin_pic,
                    'Diabetes - Type I'
                FROM tbl_clinicaldata
                WHERE diabetes = 1
            )
            UNION
            (
                SELECT
                    radar_no,
                    date_clin_pic,
                    'Diabetes - Type II'
                FROM tbl_clinicaldata
                WHERE diabetes = 2
            )
        ) AS x
        JOIN patient ON (
            x.radar_no = patient.radarNo AND
            patient.unitcode NOT IN {0}
        )
        LEFT JOIN rdr_radar_number ON patient.radarNo = rdr_radar_number.id
        LEFT JOIN tbl_demographics ON patient.radarNo = tbl_demographics.radar_no
    """.format(EXCLUDED_UNITS)

    rows = old_conn.execute(text(q))

    for row in rows:
        radar_no, from_date, diagnosis_name = row

        diagnosis_id = m.get_diagnosis_id(diagnosis_name)

        new_conn.execute(
            tables.patient_diagnoses.insert(),
            patient_id=radar_no,
            source_group_id=m.get_primary_hospital_id(radar_no),
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
    src_conn = create_engine(src).connect()
    dest_conn = create_engine(dest).connect()

    with dest_conn.begin():
        migrate_diagnoses(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
