from sqlalchemy import text, create_engine
import click

from radar_migration import Migration, tables, EXCLUDED_UNITS


def migrate_patient_aliases(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT
          radarNo,
          surnameAlias
        FROM patient
        WHERE
            radarNo is not NULL AND
            unitcode NOT IN %s AND
            surnameAlias is not NULL AND
            surnameAlias != '-'
    """ % EXCLUDED_UNITS))

    for radar_no, last_name in rows:
        new_conn.execute(
            tables.patient_aliases.insert(),
            patient_id=radar_no,
            source_group_id=m.group_id,
            source_type=m.radar_source_type,
            last_name=last_name,
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
        migrate_patient_aliases(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
