from sqlalchemy import create_engine
import click

from radar_migration import tables


def create_migration_user(conn):
    conn.execute(tables.users.insert(), username='migration')


@click.command()
@click.argument('dest')
def cli(dest):
    engine = create_engine(dest)
    conn = engine.connect()

    create_migration_user(conn)


if __name__ == '__main__':
    cli()
