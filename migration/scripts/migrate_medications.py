from sqlalchemy import text, create_engine
import click

from radar_migration import Migration, tables


def migrate_medications(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT
            patient.radarNo,
            startdate,
            enddate,
            name,
            dose
        FROM medicine
        JOIN patient ON medicine.nhsno = patient.nhsno
        WHERE
            patient.radarNo is not NULL AND
            startdate is not NULL AND
            startdate != '0000-00-00 00:00:00'
    """))

    # TODO unitcode
    for row in rows:
        new_conn.execute(
            tables.medications.insert(),
            patient_id=row['radarNo'],
            data_source_id=m.data_source_id,  # TODO
            from_date=row['startdate'],
            to_date=row['enddate'],
            name=row['name'],
            unstructured=row['dose'],
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

    migrate_medications(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
