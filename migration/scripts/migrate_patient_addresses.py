from sqlalchemy import text, create_engine
import click

from radar_migration import Migration, tables, EXCLUDED_UNITS


def migrate_patient_addresses(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT
          radarNo,
          address1,
          address2,
          address3,
          postcode
        FROM patient
        WHERE
            radarNo is not NULL AND
            unitcode NOT IN %s AND
            (
                COALESCE(address1, '') != '' OR
                COALESCE(address2, '') != '' OR
                COALESCE(address3, '') != '' OR
                COALESCE(postcode, '') != ''
            )
    """ % EXCLUDED_UNITS))

    for row in rows:
        new_conn.execute(
            tables.patient_addresses.insert(),
            patient_id=row['radarNo'],
            source_group_id=m.radar_group_id,
            source_type=m.radar_source_type,
            address_1=row['address1'],
            address_2=row['address2'],
            address_3=row['address3'],
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

    with dest_conn.begin():
        migrate_patient_addresses(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
