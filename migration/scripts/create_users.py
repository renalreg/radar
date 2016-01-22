from sqlalchemy import create_engine
import click

from radar_migration import tables


def create_migration_user(conn):
    conn.execute(tables.users.insert(), username='migration')


@click.command()
@click.argument('db')
def cli(db):
    engine = create_engine(db)
    conn = engine.connect()

    with conn.begin():
        create_migration_user(conn)


if __name__ == '__main__':
    cli()
