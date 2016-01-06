from sqlalchemy import text, create_engine
import click

from radar_migration import Migration, tables


def migrate_patient_addresses(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT
          b.radarNo,
          a.address1,
          a.address2,
          a.address3,
          a.postcode
        FROM patient AS a
        JOIN patient AS b ON a.nhsno = b.nhsno
        WHERE
            b.radarNo is not NULL AND
            COALESCE(a.address1, '') != '' AND
            COALESCE(a.address2, '') != '' AND
            COALESCE(a.address3, '') != '' AND
            COALESCE(a.postcode, '') != '' AND
            a.sourceType = 'Radar'
    """))

    for row in rows:
        new_conn.execute(
            tables.patient_addresses.insert(),
            patient_id=row['radarNo'],
            data_source_id=m.data_source_id,
            address1=row['address1'],
            address2=row['address2'],
            address3=row['address3'],
            postcode=row['postcode'],
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

    migrate_patient_addresses(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
