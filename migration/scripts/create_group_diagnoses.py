import csv

import click
from sqlalchemy import create_engine, text

from radar_migration import tables, Migration


def create_group_diagnoses(conn, filename):
    m = Migration(conn)

    with open(filename, 'rb') as f:
        reader = csv.reader(f)

        for cohort_code, diagnosis_name in reader:
            cohort_id = m.get_cohort_id(cohort_code)
            diagnosis_id = m.get_diagnosis_id(diagnosis_name)

            conn.execute(
                tables.group_diagnoses.insert(),
                group_id=cohort_id,
                diagnosis_id=diagnosis_id,
                type='PRIMARY',
            )

    rows = conn.execute(text("""
        SELECT
            code
        FROM groups
        WHERE
            type = 'COHORT' AND
            NOT EXISTS (SELECT 1 FROM group_diagnoses WHERE group_diagnoses.group_id = groups.id)
    """))

    for row in rows:
        print '%s code is missing from group diagnoses' % row[0]


@click.command()
@click.argument('db')
@click.argument('group_diagnoses')
def cli(db, group_diagnoses):
    engine = create_engine(db)
    conn = engine.connect()

    with conn.begin():
        create_group_diagnoses(conn, group_diagnoses)


if __name__ == '__main__':
    cli()
