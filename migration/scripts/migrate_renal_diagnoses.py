from sqlalchemy import text, create_engine
import click

from radar_migration import Migration, tables, EXCLUDED_UNITS


def migrate_renal_diagnoses(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT
            patient.radarNo,
            date_esrf
        FROM tbl_diagnosis
        JOIN patient ON (
            tbl_diagnosis.radar_no = patient.radarNo AND
            patient.unitcode NOT IN %s
        )
        WHERE date_esrf IS NOT NULL
    """ % EXCLUDED_UNITS))

    for radar_no, esrf_date in rows:
        new_conn.execute(
            tables.renal_diagnoses.insert(),
            patient_id=radar_no,
            esrf_date=esrf_date,
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
        migrate_renal_diagnoses(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
