from sqlalchemy import text, create_engine
import click

from radar_migration import Migration, tables


def migrate_hospitalisations(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT
            RADAR_NO,
            DATE_ADMIT,
            DATE_DISCHARGE,
            REASON_ADMIT,
            COMMENT
        FROM tbl_hospitalisation
        JOIN patient ON tbl_hospitalisation.RADAR_NO = patient.radarNo
    """))

    for row in rows:
        new_conn.execute(
            tables.hospitalisations.insert(),
            patient_id=row['RADAR_NO'],
            data_source_id=m.data_source_id,  # TODO
            date_of_admission=row['DATE_ADMIT'],
            date_of_discharge=row['DATE_DISCHARGE'],
            reason_for_admission=row['REASON_ADMIT'],
            comments=row['COMMENT'],
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

    migrate_hospitalisations(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
