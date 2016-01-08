from sqlalchemy import text, create_engine
import click

from radar_migration import Migration, tables, EXCLUDED_UNITS


def migrate_alport(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT
            rdr_alport_deafness.radar_no,
            evidenceOfDeafness,
            dateProblemFirstNoticed,
            dateStartedUsingHearingAid,
            CAST(LEAST(
                COALESCE(patient.dateReg, NOW()),
                COALESCE(rdr_radar_number.creationDate, NOW()),
                COALESCE(tbl_demographics.DATE_REG, NOW())
            ) AS DATE) AS dateReg
        FROM rdr_alport_deafness
        JOIN patient ON (
            rdr_alport_deafness.radar_no = patient.radarNo AND
            patient.unitcode NOT IN %s
        )
        LEFT JOIN rdr_radar_number ON patient.radarNo = rdr_radar_number.id
        LEFT JOIN tbl_demographics ON patient.radarNo = tbl_demographics.radar_no
    """ % EXCLUDED_UNITS))

    for row in rows:
        new_conn.execute(
            tables.alport_clinical_pictures.insert(),
            patient_id=row['radar_no'],
            date_of_picture=row['dateReg'],
            deafness=row['evidenceOfDeafness'],
            deafness_date=row['dateProblemFirstNoticed'],
            hearing_aid_date=row['dateStartedUsingHearingAid'],
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
        migrate_alport(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
