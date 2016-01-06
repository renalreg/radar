from sqlalchemy import create_engine
import click

from radar_migration.cohorts import create_cohort
from radar_migration.organisations import create_organisation
from radar_migration import tables


def bootstrap(conn):
    organisation_id = create_organisation(conn, {
        'code': 'RADAR',
        'type': 'OTHER',
        'name': 'RaDaR',
        'recruitment': True,
    })

    conn.execute(
        tables.data_sources.insert(),
        organisation_id=organisation_id,
        type='RADAR',
    )

    create_cohort(conn, {
        'code': 'RADAR',
        'name': 'RaDaR',
        'short_name': 'RaDaR',
        'features': [
            'DEMOGRAPHICS',
            'CONSULTANTS',
            'COHORTS',
            'UNITS'
        ],
    })


@click.command()
@click.argument('db')
def cli(db):
    engine = create_engine(db)
    conn = engine.connect()

    with conn.begin():
        bootstrap(conn)


if __name__ == '__main__':
    cli()
