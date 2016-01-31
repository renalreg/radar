from sqlalchemy import create_engine, text
import click

from radar_migration import EXCLUDED_UNITS, Migration, tables
from radar_migration.groups import convert_cohort_code


DIAGNOSIS_MAP = {
    '1383': 'Systemic Vasculitis - ANCA Negative - Histologially Proven',
    '1396': 'Systemic Vasculitis - ANCA Positive - No Histology',
    '1639': 'Multicystic Dysplastic Kidneys',
    '1656': 'Glomerulocystic Disease',
    '2756': 'Alport Syndrome - No Histology',
    '2760': 'Alport Syndrome - Histologically Proven',
    '2787': 'Thin Basement Membrane Disease',
    '2964': None,
    '3139': 'Diabetes - Type II MODY - Inherited/Genetic',
    '3604': None,
    '3627': 'Renal Cysts & Diabetes Syndrome',
    'APRT01': None,
    'DENTLOWE01': 'Dent Disease',
    'DENTLOWE02': 'Lowe Syndrome (Oculocerebrorenal Syndrome)',
    'DENTLOWE03': 'Other Primary Renal Fanconi Syndrome',
    'Obs': None,
    'xAHUS': None,
    'xARPKD': None,
    'xCALCIP': None,
    'xCYSURIA': None,
    'xFUAN': None,
    'xHYPALK': None,
    'xHYPALK01': 'Bartter Syndrome - Type 1',  # Note: 1/2 map to 1
    'xHYPALK02': 'Bartter Syndrome - Type 3',
    'xHYPALK03': 'Bartter Syndrome - Type 4a',  # Note: 4 to 4a
    'xHYPALK04': 'EAST Syndrome',
    'xHYPALK05': 'Gitelman Syndrome',
    'xHYPALK06': None,  # Note: not specified
    'xHYPALK07': 'Liddle Syndrome',
    'xHYPERRDG': None,
    'xIGANEPHRO': None,
    'xMEMRDG': None,
    'xPRCA': None,
    'xSTECHUS': None,
}

GROUP_DIAGNOSIS_MAP = {
    'ALPORT': 'Alport Syndrome',
    'ALPORT': 'Thin Basement Membrane Disease',
    'APRT': 'APRT Deficiency',
    'ADPKD': 'Autosomal Dominant Polycystic Kidney Disease',
    'ARPKD': 'Autosomal Recessive Polycystic Kidney Disease',
    'AHUS': 'Atypical Haemolytic Uraemic Syndrome',
    'CALCIP': 'Calciphylaxis',
    'CYSTIN': 'Cystinosis',
    'CYSURIA': 'Cystinuria',
    'DENTLOWE': 'Dent Disease and Lowe Syndrome',
    'FUAN': 'Familial Urate Associated Nephropathy',
    'HNF1B': 'HNF1b Mutations',
    'HYPOXAL': 'Hyperoxaluria',
    'HYPALK': 'Hypokalaemic Alkalosis',
    'IGANEPHRO': 'IgA Nephropathy',
    'INS': 'Idiopathic Nephrotic Syndrome',
    'MPGN': 'Membranoproliferative Glomerulonephritis / Dense Deposit Disease',
    'MEMNEPHRO': 'Membranous Nephropathy',
    'OBS': 'Pregnancy',
    'PRCA': 'Pure Red Cell Aplasia',
    'STECHUS': 'STEC-associated HUS',
    'VAS': 'Vasculitis',
}


def migrate_diagnoses(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT DISTINCT
            patient.radarNo AS radar_no,
            unit.unitcode AS cohort_code,
            tbl_diagnosis.TODO as symptoms_date,
            CASE
                WHEN tbl_diagnosis.date_diag IS NOT NULL THEN
                    tbl_diagnosis.date_diag
                WHEN patient.dateOfGenericDiagnosis IS NOT NULL THEN
                    patient.dateOfGenericDiagnosis
                ELSE
                    -- Use registration date if from date is missing
                    CAST(LEAST(
                        COALESCE(patient.dateReg, NOW()),
                        COALESCE(rdr_radar_number.creationDate, NOW()),
                        COALESCE(tbl_demographics.DATE_REG, NOW())
                    ) AS DATE)
            END AS from_date,
            patient.genericDiagnosis AS diagnosis1,
            tbl_diagnosis.steroid_resist AS diagnosis2,
            tbl_diagnosis.diag_txt AS comments,
            tbl_diagnosis.BX_PROVEN_DIAG AS biopsy_diagnosis
        FROM patient
        LEFT JOIN tbl_diagnosis ON patient.radarNo = tbl_diagnosis.radar_no
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
        radar_no = row['radar_no']
        cohort_code = convert_cohort_code(row['cohort_code'])
        comments = row['comments']
        symptoms_date = row['symptoms_date']
        from_date = row['from_date']
        diagnosis1 = row['diagnosis1']
        diagnosis2 = row['diagnosis2']
        biopsy = None
        biopsy_diagnosis = None

        diagnosis_id = None

        if cohort_code == 'INS':
            if row['biopsy_diagnosis'] == '2':
                biopsy = True
                biopsy_diagnosis = 1  # Minimal Change
            elif row['biopsy_diagnosis'] == '3':
                biopsy = True
                biopsy_diagnosis = 2  # FSGS
            elif row['biopsy_diagnosis'] == '4':
                biopsy = True
                biopsy_diagnosis = 3  # Mesangial Hyperthrophy
            elif row['biopsy_diagnosis'] == '5':
                biopsy = True
                biopsy_diagnosis = 4  # Other

            if diagnosis2 is not None:
                if diagnosis2 == 1:
                    diagnosis_id = m.get_diagnosis_id('SRNS - Primary Steroid Resistance')
                elif diagnosis2 == 2:
                    diagnosis_id = m.get_diagnosis_id('SRNS - Secondary Steroid Resistance')
                elif diagnosis2 == 3:
                    diagnosis_id = m.get_diagnosis_id('SRNS - Presumed Steroid Resistance')
        elif cohort_code == 'MPGN':
            if row['biopsy_diagnosis'] == '1':
                biopsy = True

        if diagnosis_id is None and diagnosis1 is not None:
            diagnosis_name = DIAGNOSIS_MAP[diagnosis1]

            if diagnosis_name is not None:
                diagnosis_id = m.get_diagnosis_id(diagnosis_name)

        if diagnosis_id is None:
            diagnosis_name = GROUP_DIAGNOSIS_MAP[cohort_code]
            diagnosis_id = m.get_diagnosis_id(diagnosis_name)

        new_conn.execute(
            tables.patient_diagnoses.insert(),
            patient_id=radar_no,
            source_group_id=m.group_id,
            source_type=m.radar_source_type,
            diagnosis_id=diagnosis_id,
            diagnosis_text=None,
            symptoms_date=symptoms_date,
            from_date=from_date,
            to_date=None,
            gene_test=None,
            biochemistry=None,
            clinical_picture=None,
            biopsy=biopsy,
            biopsy_diagnosis=biopsy_diagnosis,
            comments=comments,
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
