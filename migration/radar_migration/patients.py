from sqlalchemy import text

from radar_migration.constants import ETHNICITY_MAP
from radar_migration import tables


def convert_ethnicity(old_value):
    if old_value:
        new_value = ETHNICITY_MAP[old_value.upper().ljust(5, '.')]
    else:
        new_value = None

    return new_value


def convert_gender(old_value):
    if old_value in ['M', 'Male']:
        new_value = 1
    elif old_value in ['F', 'Female']:
        new_value = 2
    else:
        new_value = None

    return new_value


def migrate_patients(migration, old_conn, new_conn):
    rows = old_conn.execute(text("""
        SELECT
            a.radarNo,
            patient.nhsno,
            patient.forename,
            patient.surname,
            patient.dateofbirth,
            patient.sex,
            patient.ethnicGp,
            patient.telephone1,
            patient.mobile,
            patient.address1,
            patient.address2,
            patient.address3,
            patient.postcode,
            a.unitcode as radar_unit_code,
            a.dateReg as radar_date_registered
        FROM patient
        JOIN (
            SELECT
                patient.nhsno,
                patient.radarNo,
                patient.dateReg,
                patient.unitcode
            FROM patient
            WHERE patient.radarNo IS NOT NULL AND patient.sourceType = 'RADAR'
        ) AS a ON patient.nhsno = a.nhsno
        LEFT JOIN (
            SELECT
                nhsno,
                unitcode,
                max(date) as load_date
            FROM log
            WHERE action = 'patient data load'
            GROUP BY nhsno, unitcode
        ) AS b ON (patient.nhsno = b.nhsno and patient.unitcode = b.unitcode)
        ORDER BY
            patient.nhsno,
            (CASE WHEN patient.sourceType = 'PatientView' THEN 0 ELSE 1 END), -- prefer PatientView patients
            b.load_date DESC -- newer data first
    """))

    nhs_nos = set()

    for row in rows:
        nhs_no = row['nhsno']

        # Use the first patient row for each nhsno
        if nhs_no in nhs_nos:
            continue
        else:
            nhs_nos.add(nhs_no)

        patient_id = row['radarNo']

        # Create a patient
        new_conn.execute(
            tables.patients.insert(),
            id=patient_id,
            created_user_id=migration.user_id,
            modified_user_id=migration.user_id,
        )

        organisation_id = migration.get_organisation_id('UNIT', row['radar_unit_code'])
        recruited_date = row['radar_date_registered']

        # Add the patient to the RaDaR cohort
        new_conn.execute(
            tables.cohort_patients.insert(),
            cohort_id=migration.cohort_id,
            patient_id=patient_id,
            recruited_organisation_id=organisation_id,
            created_date=recruited_date,
            modified_date=recruited_date,
        )

        # Add RaDaR demographics
        new_conn.execute(
            tables.patient_demographics.insert(),
            patient_id=patient_id,
            data_source_id=migration.data_source_id,
            first_name=row['forename'],
            last_name=row['surname'],
            date_of_birth=row['dateofbirth'],
            gender=convert_gender(row['sex']),
            ethnicity=convert_ethnicity(row['ethnicGp']),
            home_number=row['telephone1'],
            mobile_number=row['mobile'],
            created_user_id=migration.user_id,
            modified_user_id=migration.user_id,
        )

        # Check if the patient has an address
        if any(row[x] for x in ['address1', 'address2', 'address3', 'postcode']):
            # Add the address
            new_conn.execute(
                tables.patient_addresses.insert(),
                patient_id=patient_id,
                data_source_id=migration.data_source_id,
                address1=row['address1'],
                address2=row['address2'],
                address3=row['address3'],
                postcode=row['postcode'],
                created_user_id=migration.user_id,
                modified_user_id=migration.user_id,
            )

        hospital_number = row['radar_hospital_number']

        if hospital_number:
            # Add the patient's hospital number
            new_conn.execute(
                tables.patient_numbers.insert(),
                data_source_id=migration.data_source_id,
                organisation_id=organisation_id,
                number=hospital_number,
            )

        # TODO nhsno/nhsNoType
