from sqlalchemy import text, create_engine
import click

from radar_migration import Migration, tables, EXCLUDED_UNITS


def migrate_genetics(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT
            patient.radarNo,
            labWhereTestWasDone,
            referenceNumber,
            whatResultsShowed,
            keyEvidence,
            CASE
                WHEN dateSent IS NOT NULL AND dateSent != '0000-00-00 00:00:00' THEN
                    dateSent
                ELSE
                    -- Use registration date if date sent is missing
                    CAST(LEAST(
                        COALESCE(patient.dateReg, NOW()),
                        COALESCE(rdr_radar_number.creationDate, NOW()),
                        COALESCE(tbl_demographics.DATE_REG, NOW())
                    ) AS DATE)
            END AS dateSent,
            testDoneOn,
            (
                SELECT karyotype FROM tbl_diagnosis WHERE tbl_diagnosis.radar_no = rdc_genetic_test.radar_no)
            ) AS karyotype
        FROM rdc_genetic_test
        JOIN patient ON (
            rdc_genetic_test.radar_no = patient.radarNo AND
            patient.unitcode NOT IN %s
        )
        LEFT JOIN rdr_radar_number ON patient.radarNo = rdr_radar_number.id
        LEFT JOIN tbl_demographics ON patient.radarNo = tbl_demographics.radar_no
    """ % EXCLUDED_UNITS))

    for row in rows:
        radar_no = row['radar_no']

        summary = [row['testDoneOn'], row['keyEvidence']]
        summary = [x for x in summary if x]

        if summary:
            summary = '\n'.join(summary)
        else:
            summary = None

        new_conn.execute(
            tables.genetics.insert(),
            patient_id=radar_no,
            group_id=m.get_primary_cohort_id(radar_no),
            date_sent=row['dateSent'],
            laboratory=row['labWhereTestWasDone'],
            reference_number=row['referenceNumber'],
            karyotype=row['karyotype'],
            results=row['whatResultsShowed'],
            summary=summary,
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
        migrate_genetics(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
