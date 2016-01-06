from sqlalchemy import text, create_engine
import click

from radar_migration import Migration, tables


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
            b.radarNo is not NULL AND
            a.hospitalnumber is not NULL
        ORDER BY b.radarNo
    """))

    seen_numbers = set()

    for row in rows:
        organisation_id = m.get_organisation_id('UNIT', row['unitcode'])
        number = row['hospitalnumber']

        if number in seen_numbers:
            continue
        else:
            seen_numbers.add(number)

        new_conn.execute(
            tables.patient_numbers.insert(),
            patient_id=row['radarNo'],
            data_source_id=m.data_source_id,
            organisation_id=organisation_id,
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

    migrate_patient_numbers(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
