from sqlalchemy import text, create_engine
import click

from radar_migration import Migration, tables, EXCLUDED_UNITS, GroupNotFound
from radar_migration.utils import grouper


def migrate_medications(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT
            patient.radarNo,
            startdate,
            enddate,
            name,
            dose,
            medicine.unitcode
        FROM medicine
        JOIN patient ON medicine.nhsno = patient.nhsno
        WHERE
            patient.radarNo is not NULL AND
            patient.unitcode NOT IN %s AND
            startdate is not NULL AND
            startdate != '0000-00-00 00:00:00' AND
            medicine.unitcode != 'ECS'
    """ % EXCLUDED_UNITS))

    for i, rows in enumerate(grouper(1000, rows)):
        print 'batch %d' % i

        batch = []

        for row in rows:
            group_code = row['unitcode']
            source_group_id = None
            source_type = None

            try:
                source_group_id = m.get_hospital_id(group_code)
                source_type = m.ukrdc_source_type
            except GroupNotFound:
                pass

            # Otherwise check the data was entered by a cohort
            if source_group_id is None:
                try:
                    m.get_cohort_id(group_code)
                except GroupNotFound:
                    print 'group', group_code, 'not found'
                    continue

                source_group_id = m.group_id
                source_type = m.radar_source_type

            batch.append(dict(
                patient_id=row['radarNo'],
                source_group_id=source_group_id,
                source_type=source_type,
                from_date=row['startdate'],
                to_date=row['enddate'],
                drug_text=row['name'],
                dose_text=row['dose'],
                created_user_id=m.user_id,
                modified_user_id=m.user_id,
            ))

        new_conn.execute(tables.medications.insert(), batch)


@click.command()
@click.argument('src')
@click.argument('dest')
def cli(src, dest):
    src_engine = create_engine(src)
    dest_engine = create_engine(dest)

    src_conn = src_engine.connect()
    dest_conn = dest_engine.connect()

    with dest_conn.begin():
        migrate_medications(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
