from sqlalchemy import create_engine
import click

from radar_migration import migrate


@click.command()
@click.argument('src')
@click.argument('dest')
def cli(src, dest):
    old_engine = create_engine(src, echo=True)
    new_engine = create_engine(dest, echo=True)
    migrate(old_engine, new_engine)


if __name__ == '__main__':
    cli()
