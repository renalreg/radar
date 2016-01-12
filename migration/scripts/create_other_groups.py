import copy

import click
from sqlalchemy import create_engine

from radar_migration.groups import create_group

GROUPS = [
    {'code': 'RADAR', 'name': 'RaDaR'},
    {'code': 'NHS', 'name': 'NHS'},
    {'code': 'CHI', 'name': 'CHI'},
    {'code': 'UKRR', 'name': 'UK Renal Registry'},
    {'code': 'HANDC', 'name': 'H&C'},
    {'code': 'UKRDC', 'name': 'UKRDC'},
    {'code': 'NHSBT', 'name': 'NHS Blood and Transplant'},
    {'code': 'BAPN', 'name': 'BAPN'},
]


def create_other_groups(conn):
    for group in GROUPS:
        group = copy.deepcopy(group)
        group['type'] = 'OTHER'
        group['short_name'] = group['name']
        create_group(conn, group)


@click.command()
@click.argument('db')
def cli(db):
    engine = create_engine(db)
    conn = engine.connect()

    with conn.begin():
        create_other_groups(conn)


if __name__ == '__main__':
    cli()
