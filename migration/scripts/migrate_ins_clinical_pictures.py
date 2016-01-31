from sqlalchemy import create_engine, text
import click

from radar_migration import Migration, tables, EXCLUDED_UNITS, bit_to_bool


def migrate_ins_clinical_pictures(old_conn, new_conn):
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
            INFECTION,
            INFECTION_DETAIL,
            THROMBOSIS,
            PERITONITIS,
            PUL_OED,
            RASH,
            RASH_DETAIL,
            HYPOVAL,
            FEVER,
            HTH_REQ_TMT,
            tbl_clinicaldata.COMMENTS,
            OPTHALM,
            OPTHALM_DETAIL,
            OEDEMA,
            PREC_INF,
            PREC_INF_DETAIL
        FROM tbl_clinicaldata
        JOIN patient ON (
            tbl_clinicaldata.radar_no = patient.radarNo AND
            patient.unitcode NOT IN {0}
        )
        LEFT JOIN rdr_radar_number ON patient.radarNo = rdr_radar_number.id
        LEFT JOIN tbl_demographics ON patient.radarNo = tbl_demographics.radar_no
        WHERE
            -- Only SRNS (INS) patients
            EXISTS (
                SELECT 1 FROM usermapping
                WHERE
                    usermapping.nhsno = patient.nhsno AND
                    usermapping.unitcode = 'SRNS'
            )
    """.format(EXCLUDED_UNITS)))

    for row in rows:
        patient_id = row['RADAR_NO']
        date_of_picture = row['DATE_CLIN_PIC']
        oedema = bit_to_bool(row['OEDEMA'])
        hypovalaemia = bit_to_bool(row['HYPOVAL'])
        fever = bit_to_bool(row['FEVER'])
        thrombosis = bit_to_bool(row['THROMBOSIS'])
        peritonitis = bit_to_bool(row['PERITONITIS'])
        pulmonary_odemea = bit_to_bool(row['PUL_OED'])
        hypertension = bit_to_bool(row['HTH_REQ_TMT'])
        rash = bit_to_bool(row['RASH'])
        rash_details = row['RASH_DETAIL']
        infection = bit_to_bool(row['PREC_INF'])
        infection_details = row['PREC_INF_DETAIL']
        ophthalmoscopy = bit_to_bool(row['OPTHALM'])
        ophthalmoscopy_details = row['OPTHALM_DETAIL']
        comments = row['COMMENTS']

        new_conn.execute(
            tables.ins_clinical_pictures.insert(),
            patient_id=patient_id,
            date_of_picture=date_of_picture,
            oedema=oedema,
            hypovalaemia=hypovalaemia,
            fever=fever,
            thrombosis=thrombosis,
            peritonitis=peritonitis,
            pulmonary_odemea=pulmonary_odemea,
            hypertension=hypertension,
            rash=rash,
            rash_details=rash_details,
            infection=infection,
            infection_details=infection_details,
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
        migrate_ins_clinical_pictures(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
