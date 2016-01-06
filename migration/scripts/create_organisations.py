import csv

import click
from sqlalchemy import create_engine

from radar_migration.organisations import create_organisation

ORGANISATIONS = [
    {'code': 'NHS', 'type': 'OTHER', 'name': 'NHS', 'recruitment': True},
    {'code': 'CHI', 'type': 'OTHER', 'name': 'CHI', 'recruitment': True},
    {'code': 'UKRR', 'type': 'OTHER', 'name': 'UK Renal Registry', 'recruitment': True},
    {'code': 'HANDC', 'type': 'OTHER', 'name': 'H&C', 'recruitment': True},
    {'code': 'UKRDC', 'type': 'OTHER', 'name': 'UKRDC', 'recruitment': True},
    {'code': 'NHSBT', 'type': 'OTHER', 'name': 'NHS Blood and Transplant', 'recruitment': True},
    {'code': 'BAPN', 'type': 'OTHER', 'name': 'BAPN', 'recruitment': True},
]


def create_organisations(conn, units_filename):
    organisations = list(ORGANISATIONS)

    with open(units_filename, 'rb') as f:
        reader = csv.reader(f)

        for code, name in reader:
            organisations.append({
                'code': code,
                'type': 'UNIT',
                'name': name,
                'recruitment': False,
            })

    for x in organisations:
        create_organisation(conn, x)


@click.command()
@click.argument('db')
@click.argument('units')
def cli(db, units):
    engine = create_engine(db)
    conn = engine.connect()

    with conn.begin():
        create_organisations(conn, units)


if __name__ == '__main__':
    cli()
