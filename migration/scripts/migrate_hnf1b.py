from sqlalchemy import text, create_engine
import click

from radar_migration import EXCLUDED_UNITS, tables, Migration


def optional_bool(old_value):
    if old_value is None:
        new_value = None
    else:
        new_value = old_value == 1

    return new_value


def migrate_hnf1b(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT
            rdr_hnf1b_misc.radar_no,
            singleKidney,
            gout,
            genitalMalformation,
            genitalMalformationDetails,
            CAST(LEAST(
                COALESCE(patient.dateReg, NOW()),
                COALESCE(rdr_radar_number.creationDate, NOW()),
                COALESCE(tbl_demographics.DATE_REG, NOW())
            ) AS DATE) AS dateReg
        FROM rdr_hnf1b_misc
        JOIN patient ON (
            rdr_hnf1b_misc.radar_no = patient.radarNo AND
            patient.unitcode NOT IN %s
        )
        LEFT JOIN rdr_radar_number ON patient.radarNo = rdr_radar_number.id
        LEFT JOIN tbl_demographics ON patient.radarNo = tbl_demographics.radar_no
    """ % EXCLUDED_UNITS))

    for row in rows:
        single_kidney = optional_bool(row['singleKidney'])
        hyperuricemia_gout = optional_bool(row['gout'])
        genital_malformation = optional_bool(row['genitalMalformation'])

        new_conn.execute(
            tables.hnf1b_clinical_pictures.insert(),
            patient_id=row['radar_no'],
            date_of_picture=row['dateReg'],
            single_kidney=single_kidney,
            hyperuricemia_gout=hyperuricemia_gout,
            genital_malformation=genital_malformation,
            genital_malformation_details=row['genitalMalformationDetails'],
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
        migrate_hnf1b(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
