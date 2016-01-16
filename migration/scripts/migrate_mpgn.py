from sqlalchemy import create_engine, text
import click

from radar_migration import Migration, EXCLUDED_UNITS, tables


def bit_to_bool(value):
    if value is None:
        r = None
    elif value == '\0':
        r = False
    elif value == '\1':
        r = True
    else:
        raise ValueError('Not a bit')

    return r


def int_to_bool(value):
    if value is None:
        r = None
    elif value == 0:
        r = False
    elif value == 1:
        r = True
    else:
        raise ValueError('Not 0 or 1')

    return r


def migrate_mpgn(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT
            tbl_clinicaldata.RADAR_NO,
            CASE
                WHEN DATE_CLIN_PIC IS NOT NULL AND DATE_CLIN_PIC != '0000-00-00 00:00:00' THEN
                    DATE_CLIN_PIC
                ELSE
                    -- Use registration date if result date is missing
                    CAST(LEAST(
                        COALESCE(patient.dateReg, NOW()),
                        COALESCE(rdr_radar_number.creationDate, NOW()),
                        COALESCE(tbl_demographics.DATE_REG, NOW())
                    ) AS DATE)
            END as DATE_CLIN_PIC,
            OEDEMA,
            HTH_REQ_TMT,
            PREC_INF,
            PREC_INF_DETAIL,
            URTICARIA,
            PART_LIPODYS,
            OPTHALM,
            OPTHALM_DETAIL,
            tbl_clinicaldata.COMMENTS
        FROM tbl_clinicaldata
        JOIN patient ON (
            tbl_clinicaldata.radar_no = patient.radarNo AND
            patient.unitcode NOT IN {0}
        )
        LEFT JOIN rdr_radar_number ON patient.radarNo = rdr_radar_number.id
        LEFT JOIN tbl_demographics ON patient.radarNo = tbl_demographics.radar_no
    """.format(EXCLUDED_UNITS)))

    for row in rows:
        patient_id = row['RADAR_NO']
        date_of_picture = row['DATE_CLIN_PIC']
        oedema = bit_to_bool(row['OEDEMA'])
        hypertension = bit_to_bool(row['HTH_REQ_TMT'])
        urticaria = int_to_bool(row['URTICARIA'])
        partial_lipodystrophy = bit_to_bool(row['PART_LIPODYS'])
        recent_infection = bit_to_bool(row['PREC_INF'])
        recent_infection_details = row['PREC_INF_DETAIL']
        ophthalmoscopy = bit_to_bool(row['OPTHALM'])
        ophthalmoscopy_details = row['OPTHALM_DETAIL']
        comments = row['COMMENTS']

        new_conn.execute(
            tables.mpgn_clinical_pictures.insert(),
            patient_id=patient_id,
            date_of_picture=date_of_picture,
            oedema=oedema,
            hypertension=hypertension,
            urticaria=urticaria,
            partial_lipodystrophy=partial_lipodystrophy,
            recent_infection=recent_infection,
            recent_infection_details=recent_infection_details,
            ophthalmoscopy=ophthalmoscopy,
            ophthalmoscopy_details=ophthalmoscopy_details,
            comments=comments,
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
        migrate_mpgn(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
