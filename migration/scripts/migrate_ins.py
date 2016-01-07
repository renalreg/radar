from sqlalchemy import create_engine, text
import click

from radar_migration import Migration, tables

KIDNEY_TYPE_MAP = {
    None: None,
    0: 'NATIVE',
    1: 'TRANSPLANT',
}

REMISSION_TYPE_MAP = {
    None: None,
    1: 'COMPLETE',
    2: 'PARTIAL',
    3: 'NONE',
    9: None,
}


def convert_kidney_type(old_value):
    try:
        new_value = KIDNEY_TYPE_MAP[old_value]
    except KeyError:
        raise ValueError('Unknown kidney type: %s' % old_value)

    return new_value


def convert_remission_type(old_value):
    try:
        new_value = REMISSION_TYPE_MAP[old_value]
    except KeyError:
        raise ValueError('Unknown remission type: %s' % old_value)

    return new_value


# TODO clinical pictures
def migrate_ins(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT
            RADAR_NO,
            DATE_ONSET_RELAP,
            RELAP_TX_NAT,
            TRIG_VIRAL,
            TRIG_IMMUN,
            TRIG_OTHER,
            REMISS_ACHIEVE,
            DATE_REMISSION
        FROM tbl_relapse
        JOIN patient ON (
            tbl_relapse.radar_no = patient.radarNo AND
            patient.unitcode NOT IN ('RENALREG', 'DEMO')
        )
    """))

    # TODO RELAP_DRUG_1, RELAP_DRUG_2, RELAP_DRUG_3
    for row in rows:
        kidney_type = convert_kidney_type(row['RELAP_TX_NAT'])
        remission_type = convert_remission_type(row['REMISS_ACHIEVE'])

        new_conn.execute(
            tables.ins_relapses.insert(),
            patient_id=row['RADAR_NO'],
            date_of_relapse=row['DATE_ONSET_RELAP'],
            kidney_type=kidney_type,
            viral_trigger=row['TRIG_VIRAL'],
            immunisation_trigger=row['TRIG_IMMUN'],
            other_trigger=row['TRIG_OTHER'],
            date_of_remission=row['DATE_REMISSION'],
            remission_type=remission_type,
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
        migrate_ins(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
