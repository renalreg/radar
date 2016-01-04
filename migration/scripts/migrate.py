from sqlalchemy import create_engine
import click

from radar_migration import migrate


@click.command()
@click.argument('src')
@click.argument('dest')
@click.option('--units', default='units.csv')
@click.option('--organisations', default='organisations.csv')
@click.option('--cohorts', default='cohorts.csv')
def cli(src, dest, units, organisations, cohorts):
    old_engine = create_engine(src, echo=True)
    new_engine = create_engine(dest, echo=True)
    migrate(
        old_engine,
        new_engine,
        units_filename=units,
        organisations_filename=organisations,
        cohorts_filename=cohorts,
    )


if __name__ == '__main__':
    cli()
