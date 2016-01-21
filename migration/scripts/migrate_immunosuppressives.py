from sqlalchemy import text, create_engine
import click

from radar_migration import Migration, tables, EXCLUDED_UNITS


IMMMUNOSUPPRESSIVE_MAP = {
    1: 'Corticosteroids',
    2: 'Myophenolate Mofetil - MMF',
    3: 'Azathioprine',
    4: 'Ciclosporin',
    6: 'Tacrolimus',
    7: 'Sirolimus',
    8: 'Cyclophosphamide',
    10: 'Rituximab',
    11: 'Alemtuzumab',
    12: 'Daclizumab',
    13: 'Basiliximab',
    14: 'Eculizumab',
    15: 'Levamisole',
    88: 'Immunosuppressive',
}


def migrate_immunosuppressives(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT
            patient.radarNo,
            IMMUNSUP_DRUG_STARTDATE,
            IMMUNSUP_DRUG_ENDDATE,
            IMMUNSUP_DRUG,
            CYCLOPHOS_TOT_DOSE
        FROM tbl_immunsup_treatment
        JOIN patient ON tbl_immunsup_treatment.radar_no = patient.radarNo
        WHERE
            patient.radarNo IS NOT NULL AND
            patient.unitcode NOT IN %s
    """ % EXCLUDED_UNITS))

    for radar_no, from_date, to_date, old_drug_id, dose_quantity in rows:
        new_drug_name = IMMMUNOSUPPRESSIVE_MAP[old_drug_id]
        new_drug_id = m.get_drug_id(new_drug_name)

        new_conn.execute(
            tables.medications.insert(),
            patient_id=radar_no,
            source_group_id=m.radar_group_id,  # TODO
            source_type=m.radar_source_type,
            from_date=from_date,
            to_date=to_date,
            drug_id=new_drug_id,
            dose_quantity=dose_quantity,
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
        migrate_immunosuppressives(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
