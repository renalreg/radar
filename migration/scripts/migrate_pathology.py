from sqlalchemy import text, create_engine
import click

from radar_migration import Migration, tables


def convert_kidney_type(old_value):
    if old_value is None:
        new_value = None
    elif old_value == 0:
        new_value = 'NATIVE'
    elif old_value == 1:
        new_value = 'TRANSPLANT'
    else:
        raise ValueError('Unknown kidney type: %s' % old_value)

    return new_value


def convert_kidney_side(old_value):
    if old_value is None:
        new_value = None
    elif old_value == 1:
        new_value = 'LEFT'
    elif old_value == 2:
        new_value = 'RIGHT'
    else:
        raise ValueError('Unknown kidney side: %s' % old_value)

    return new_value


def migrate_pathology(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT
            RADAR_NO,
            BX_DATE,
            NAT_TRANSP_KID,
            LATERALITY_BX,
            SAMPLE_LAB_NO,
            PATH_TXT
        FROM tbl_pathology
        JOIN patient ON tbl_pathology.RADAR_NO = patient.radarNo
    """))

    for row in rows:
        kidney_type = convert_kidney_type(row['NAT_TRANSP_KID'])
        kidney_side = convert_kidney_side(row['LATERALITY_BX'])

        # TODO other fields
        new_conn.execute(
            tables.pathology.insert(),
            patient_id=row['RADAR_NO'],
            data_source_id=m.data_source_id,  # TODO
            date=row['BX_DATE'],
            kidney_type=kidney_type,
            kidney_side=kidney_side,
            laboratory_reference_number=row['SAMPLE_LAB_NO'],
            histological_summary=row['PATH_TXT'],
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

    migrate_pathology(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
