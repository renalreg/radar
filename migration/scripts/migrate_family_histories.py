from sqlalchemy import text, create_engine, select
import click

from radar_migration import Migration, tables, EXCLUDED_UNITS

PARENTAL_CONSANGUINITY_MAP = {
    None: None,
    0: False,
    1: True,
    9: None,
}

FAMILY_HISTORY_MAP = {
    None: None,
    0: False,
    1: True,
    9: None,
    99: None,
}


def convert_parental_consanguity(old_value):
    try:
        new_value = PARENTAL_CONSANGUINITY_MAP[old_value]
    except KeyError:
        raise ValueError('Unknown parental consanguity: %s' % old_value)

    return new_value


def convert_family_history(old_value):
    try:
        new_value = FAMILY_HISTORY_MAP[old_value]
    except KeyError:
        raise ValueError('Unknown family history: %s' % old_value)

    return new_value


def check_patient_exists(conn, patient_id):
    q = select().where(tables.patients.c.id == patient_id)
    return conn.execute(q).fetchone() is not None


def migrate_family_histories(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT
            RADAR_NO,
            CONSANGUINITY,
            FAM_HIST,
            REL1,
            REL1_RADAR,
            REL2,
            REL2_RADAR,
            REL3,
            REL3_RADAR,
            REL4,
            REL4_RADAR,
            REL5,
            REL5_RADAR,
            REL6,
            REL6_RADAR
        FROM tbl_diagnosis
        JOIN patient ON (
            tbl_diagnosis.RADAR_NO = patient.radarNo AND
            patient.unitcode NOT IN %s
        )
    """ % EXCLUDED_UNITS))

    for row in rows:
        parental_consanguinity = convert_parental_consanguity(row['CONSANGUINITY'])
        family_history = convert_family_history(row['FAM_HIST'])

        result = new_conn.execute(
            tables.family_histories.insert(),
            patient_id=row['RADAR_NO'],
            cohort_id=m.cohort_id,  # TODO
            parental_consanguinity=parental_consanguinity,
            family_history=family_history,
            created_user_id=m.user_id,
            modified_user_id=m.user_id,
        )

        family_history_id = result.inserted_primary_key[0]

        for relationship, radar_no in [(row['REL%d' % x], row['REL%d_RADAR' % x]) for x in range(1, 7)]:
            if relationship is None:
                continue

            if radar_no is not None and not check_patient_exists(new_conn, radar_no):
                radar_no = None

            new_conn.execute(
                tables.family_history_relatives.insert(),
                family_history_id=family_history_id,
                relationship=relationship,
                patient_id=radar_no,
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
        migrate_family_histories(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
