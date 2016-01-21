import csv

from sqlalchemy import create_engine, exists, select
import click

from radar_migration import Migration, tables, check_patient_exists


def add_patients_to_group(conn, group_type, group_code, patients_filename):
    m = Migration(conn)

    group_id = m.get_group_id(group_type, group_code)

    with open(patients_filename, 'rb') as f:
        reader = csv.reader(f)

        for row in reader:
            patient_id = int(row[0])

            if not check_patient_exists(conn, patient_id):
                print '%d not found' % patient_id
                continue

            q = exists()
            q = q.where(tables.group_patients.c.patient_id == patient_id)
            q = q.where(tables.group_patients.c.group_id == group_id)
            q = select([q])

            in_group = conn.execute(q).fetchone()[0]

            # Patient is already in the group
            if in_group:
                print '%d already in group' % patient_id
            else:
                conn.execute(
                    tables.group_patients.insert(),
                    patient_id=patient_id,
                    group_id=group_id,
                    from_date=m.now,
                    created_group_id=m.get_recruited_group_id(patient_id),
                    created_user_id=m.user_id,
                    modified_user_id=m.user_id
                )


@click.command()
@click.argument('db')
@click.argument('group_type')
@click.argument('group_code')
@click.argument('patients')
def cli(db, group_type, group_code, patients):
    engine = create_engine(db)
    conn = engine.connect()

    with conn.begin():
        add_patients_to_group(conn, group_type, group_code, patients)


if __name__ == '__main__':
    cli()
