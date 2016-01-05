from sqlalchemy import text, create_engine
import click

from radar_migration import Migration, tables


# TODO
MODALITY_MAP = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    9: 0,
    10: 0,
    11: 0,
    12: 0,
    13: 0,
    14: 0,
    17: 0,
    19: 0,
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
        JOIN patient ON tbl_rrt_treatment.RADAR_NO = patient.radarNo
    """))

    # TODO UNIT_CODE
    for row in rows:
        modality = convert_modality(row['MODALITY'])

        new_conn.execute(
            tables.dialysis.insert(),
            patient_id=row['RADAR_NO'],
            data_source_id=m.data_source_id,  # TODO
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

    migrate_dialysis(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
