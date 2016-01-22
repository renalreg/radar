import copy

import click
from sqlalchemy import create_engine

from radar_migration.groups import create_group

GROUPS = [
    {'code': 'NHS', 'name': 'NHS', 'recruitment': True},
    {'code': 'CHI', 'name': 'CHI', 'recruitment': True},
    {'code': 'HANDC', 'name': 'H&C', 'recruitment': True},
    {'code': 'RADAR', 'name': 'RaDaR'},
    {'code': 'UKRR', 'name': 'UK Renal Registry'},
    {'code': 'UKRDC', 'name': 'UKRDC'},
    {'code': 'NHSBT', 'name': 'NHS Blood and Transplant'},
    {'code': 'BAPN', 'name': 'BAPN'},
]


def create_other_groups(conn):
    for group in GROUPS:
        group = copy.deepcopy(group)
        group['type'] = 'OTHER'
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
