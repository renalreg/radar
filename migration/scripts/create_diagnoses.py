import csv

import click
from sqlalchemy import create_engine

from radar_migration.groups import tables


def create_diagnoses(conn, diagnoses_filename):
    with open(diagnoses_filename, 'rb') as f:
        reader = csv.reader(f)

        for row in reader:
            name = row[0]

            conn.execute(
                tables.diagnoses.insert(),
                name=name
            )


@click.command()
@click.argument('db')
@click.argument('diagnoses')
def cli(db, diagnoses):
    engine = create_engine(db)
    conn = engine.connect()

    with conn.begin():
        create_diagnoses(conn, diagnoses)


if __name__ == '__main__':
    cli()
