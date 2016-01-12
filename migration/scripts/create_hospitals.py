import csv

import click
from sqlalchemy import create_engine

from radar_migration.groups import create_group


def create_hospitals(conn, hospitals_filename):
    with open(hospitals_filename, 'rb') as f:
        reader = csv.reader(f)

        for code, name in reader:
            create_group(conn, {
                'code': code,
                'type': 'HOSPITAL',
                'name': name,
                'short_name': name,
            })


@click.command()
@click.argument('db')
@click.argument('hospitals')
def cli(db, hospitals):
    engine = create_engine(db)
    conn = engine.connect()

    with conn.begin():
        create_hospitals(conn, hospitals)


if __name__ == '__main__':
    cli()
