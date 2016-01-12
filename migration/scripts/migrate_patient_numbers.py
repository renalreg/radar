from sqlalchemy import text, create_engine
import click

from radar_migration import Migration, tables, EXCLUDED_UNITS


def migrate_patient_numbers(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT
          b.radarNo,
          a.unitcode,
          a.hospitalnumber
        FROM patient AS a
        JOIN patient AS b ON a.nhsno = b.nhsno
        WHERE
            b.radarNo IS NOT NULL AND
            b.unitcode NOT IN %s AND
            a.hospitalnumber iS NOT NULL
        ORDER BY b.radarNo
    """ % EXCLUDED_UNITS))

    seen_numbers = set()

    for row in rows:
        hospital_id = m.get_hospital_id(row['unitcode'])
        number = row['hospitalnumber']

        if number in seen_numbers:
            continue
        else:
            seen_numbers.add(number)

        new_conn.execute(
            tables.patient_numbers.insert(),
            patient_id=row['radarNo'],
            source_group_id=m.group_id,
            source_type=m.source_type,
            number_group_id=hospital_id,
            number=number,
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
        migrate_patient_numbers(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
