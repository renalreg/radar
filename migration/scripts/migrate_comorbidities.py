from sqlalchemy import create_engine, text
import click

from radar_migration import Migration, tables, EXCLUDED_UNITS


def migrate_comorbidities(old_conn, new_conn):
    m = Migration(new_conn)

    q = """
        SELECT
            comorbidities.radar_no,
            CASE
                WHEN comorbidities.from_date IS NOT NULL THEN
                    comorbidities.from_date
                ELSE
                    -- Use registration date if from date is missing
                    CAST(LEAST(
                        COALESCE(patient.dateReg, NOW()),
                        COALESCE(rdr_radar_number.creationDate, NOW()),
                        COALESCE(tbl_demographics.DATE_REG, NOW())
                    ) AS DATE)
            END as from_date,
            comorbidities.disorder_name
        FROM (
            (
                SELECT
                    radar_no as radar_no,
                    dateAtDiabetesDiagnosis as from_date,
                    'Diabetes' as disorder_name
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
        ) AS comorbidities
        JOIN patient ON (
            comorbidities.radar_no = patient.radarNo AND
            patient.unitcode NOT IN {0}
        )
        LEFT JOIN rdr_radar_number ON patient.radarNo = rdr_radar_number.id
        LEFT JOIN tbl_demographics ON patient.radarNo = tbl_demographics.radar_no
    """.format(EXCLUDED_UNITS)

    rows = old_conn.execute(text(q))

    for row in rows:
        patient_id, from_date, disorder_name = row

        disorder_id = m.get_disorder_id(disorder_name)

        new_conn.execute(
            tables.comorbidities.insert(),
            patient_id=patient_id,
            source_group_id=m.group_id,  # TODO
            source_type=m.source_type,
            disorder_id=disorder_id,
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
        migrate_comorbidities(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
