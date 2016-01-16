import csv

import click
from sqlalchemy import create_engine

from radar_migration.groups import tables


def create_disorders(conn, disorders_filename):
    with open(disorders_filename, 'rb') as f:
        reader = csv.reader(f)

        for row in reader:
            name = row[0]

            conn.execute(
                tables.disorders.insert(),
                name=name
            )


@click.command()
@click.argument('db')
@click.argument('disorders')
def cli(db, disorders):
    engine = create_engine(db)
    conn = engine.connect()

    with conn.begin():
        create_disorders(conn, disorders)


if __name__ == '__main__':
    cli()
