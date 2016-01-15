from sqlalchemy import text, create_engine
import click

from radar_migration import Migration, tables, EXCLUDED_UNITS

MODALITY_MAP = {
    1: 1,
    2: 2,
    3: 3,
    4: 1,
    5: 5,
    9: 1,
    10: 11,
    11: 11,
    12: 12,
    13: 12,
    14: 12,
    15: 12,
    16: 121,
    17: 121,
    19: 19,
}


def convert_modality(old_value):
    new_value = MODALITY_MAP.get(old_value)

    if new_value is None:
        raise ValueError('Unknown modality: %s' % old_value)

    return new_value


def migrate_dialysis(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT
            RADAR_NO,
            MODALITY,
            DATE_START,
            DATE_STOP
        FROM tbl_rrt_treatment
        JOIN patient ON (
            tbl_rrt_treatment.RADAR_NO = patient.radarNo AND
            patient.unitcode NOT IN %s
        )
    """ % EXCLUDED_UNITS))

    # TODO UNIT_CODE
    for row in rows:
        modality = convert_modality(row['MODALITY'])

        new_conn.execute(
            tables.dialysis.insert(),
            patient_id=row['RADAR_NO'],
            source_group_id=m.group_id,  # TODO
            source_type=m.source_type,
            from_date=row['DATE_START'],
            to_date=row['DATE_STOP'],
            modality=modality,
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
        migrate_dialysis(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
