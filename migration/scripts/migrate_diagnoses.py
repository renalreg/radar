from sqlalchemy import create_engine, text
import click

from radar_migration import EXCLUDED_UNITS, Migration, tables
from radar_migration.groups import convert_cohort_code


DIAGNOSIS_MAP = {
    None: None,
    '1383': 33,
    '1396': 32,
    '1639': 9,
    '1656': 8,
    '2756': 1,
    '2760': 2,
    '2787': 3,
    '2964': None,
    '3139': 10,
    '3604': None,
    '3627': 7,
    'APRT01': None,
    'DENTLOWE01': 4,
    'DENTLOWE02': 5,
    'DENTLOWE03': 6,
    'Obs': None,
    'xAHUS': None,
    'xARPKD': None,
    'xCALCIP': None,
    'xCYSURIA': None,
    'xFUAN': None,
    'xHYPALK': None,
    'xHYPALK01': 15,  # Note: 1/2 map to 1
    'xHYPALK02': 17,
    'xHYPALK03': 18,  # Note: 4 to 4a
    'xHYPALK04': 20,
    'xHYPALK05': 14,
    'xHYPALK06': None,  # Note: not specified
    'xHYPALK07': 21,
    'xHYPERRDG': None,
    'xIGANEPHRO': None,
    'xMEMRDG': None,
    'xPRCA': None,
    'xSTECHUS': None,
}


def convert_diagnosis(value):
    try:
        value = DIAGNOSIS_MAP[value]
    except KeyError:
        raise ValueError('Unknown diagnosis: %s' % value)

    return value


def migrate_diagnoses(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT DISTINCT
            patient.radarNo,
            CASE
                WHEN patient.dateOfGenericDiagnosis IS NOT NULL THEN
                    patient.dateOfGenericDiagnosis
                ELSE
                    -- Use registration date if result date is missing
                    CAST(LEAST(
                        COALESCE(patient.dateReg, NOW()),
                        COALESCE(rdr_radar_number.creationDate, NOW()),
                        COALESCE(tbl_demographics.DATE_REG, NOW())
                    ) AS DATE)
            END,
            patient.genericDiagnosis,
            unit.unitcode
        FROM patient
        JOIN usermapping ON patient.nhsno = usermapping.nhsno
        JOIN unit ON usermapping.unitcode = unit.unitcode
        LEFT JOIN rdr_radar_number ON patient.radarNo = rdr_radar_number.id
        LEFT JOIN tbl_demographics ON patient.radarNo = tbl_demographics.radar_no
        WHERE
            patient.radarNo IS NOT NULL AND
            patient.unitcode NOT IN {0} AND
            unit.sourceType = 'radargroup'
    """.format(EXCLUDED_UNITS)))

    for row in rows:
        patient_id, date_of_diagnosis, diagnosis_code, cohort_code = row

        group_diagnosis_id = convert_diagnosis(diagnosis_code)

        cohort_code = convert_cohort_code(cohort_code)
        cohort_id = m.get_cohort_id(cohort_code)

        new_conn.execute(
            tables.diagnoses.insert(),
            patient_id=patient_id,
            group_id=cohort_id,
            date_of_diagnosis=date_of_diagnosis,
            group_diagnosis_id=group_diagnosis_id,
            created_user_id=m.user_id,
            modified_user_id=m.user_id,
        )


@click.command()
@click.argument('src')
@click.argument('dest')
def cli(src, dest):
    src_conn = create_engine(src).connect()
    dest_conn = create_engine(dest).connect()

    with dest_conn.begin():
        migrate_diagnoses(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
