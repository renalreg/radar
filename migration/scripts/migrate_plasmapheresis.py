from sqlalchemy import text, create_engine
import click

from radar_migration import Migration, tables, EXCLUDED_UNITS


NO_OF_EXCHANGES_MAP = {
    '1': '1/1D',
    '2': '5/1W',
    '3': '4/1W',
    '4': '3/1W',
    '5': '2/1W',
    '6': '1/1W',
    '7': '1/2W',
    '8': '1/4W',
}

RESPONSE_MAP = {
    1: 'COMPLETE',
    2: 'PARTIAL',
    3: 'NONE',
}


def convert_no_of_exchanges(old_value):
    try:
        new_value = NO_OF_EXCHANGES_MAP[old_value]
    except KeyError:
        raise ValueError('Unknown no of exchanges: %s' % old_value)

    return new_value


def convert_response(old_value):
    try:
        new_value = RESPONSE_MAP[old_value]
    except KeyError:
        raise ValueError('Unknown response: %s' % old_value)

    return new_value


def migrate_plasmapheresis(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT
            RADAR_NO,
            DATE_START_PLASMAPH,
            DATE_STOP_PLASMAPH,
            NO_EXCH_PLASMAPH,
            RESPONSE_TO_PLASMA
        FROM tbl_rrt_plasma
        JOIN patient ON (
            tbl_rrt_plasma.RADAR_NO = patient.radarNo AND
            patient.unitcode NOT IN %s
        )
    """ % EXCLUDED_UNITS))

    for row in rows:
        no_of_exchanges = convert_no_of_exchanges(row['NO_EXCH_PLASMAPH'])
        response = convert_response(row['RESPONSE_TO_PLASMA'])

        new_conn.execute(
            tables.plasmapheresis.insert(),
            patient_id=row['RADAR_NO'],
            source_group_id=m.radar_group_id,  # TODO
            source_type=m.radar_source_type,
            from_date=row['DATE_START_PLASMAPH'],
            to_date=row['DATE_STOP_PLASMAPH'],
            no_of_exchanges=no_of_exchanges,
            response=response,
            created_user_id=m.user_id,
            modified_user_id=m.user_id,
        )


@click.command()
@click.argument('src')
@click.argument('dest')
def cli(src, dest):
    src_engine = create_engine(src)
    dest_engine = create_engine(dest)

    src_conn = src_engine.connect()
    dest_conn = dest_engine.connect()

    with dest_conn.begin():
        migrate_plasmapheresis(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
