from sqlalchemy import text, create_engine
import click

from radar_migration import EXCLUDED_UNITS


# TODO
def migrate_hnf1b(old_conn, new_conn):
    rows = old_conn.execute(text("""
        SELECT
            radar_no
        FROM rdr_hnf1b_misc
        JOIN patient ON (
            rdr_hnf1b_misc.radar_no = patient.radarNo AND
            patient.unitcode NOT IN %s
        )
    """ % EXCLUDED_UNITS))

    for row in rows:
        print row


@click.command()
@click.argument('src')
@click.argument('dest')
def cli(src, dest):
    src_engine = create_engine(src)
    dest_engine = create_engine(dest)

    src_conn = src_engine.connect()
    dest_conn = dest_engine.connect()

    with dest_conn.begin():
        migrate_hnf1b(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
