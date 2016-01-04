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


def number_to_organisation_code(value):
    if len(value) != 10 or not value.isdigit():
        return None
    elif value > '0101000000' and value < '3112999999':
        return 'CHI'
    elif value > '3200000010' and value < '3999999999':
        return 'HANDC'
    else:
        return 'NHS'


def migrate_patients(migration, old_conn, new_conn):
    rows = old_conn.execute(text("""
        SELECT
            r.radarNo AS 'radar_no',
            r.nhsno AS 'nhs_no',
            r.unitcode AS 'unit_code',
            r.dateReg AS 'date_registered',
            r.hospitalnumber AS 'hospital_number',
            user.username AS 'username',
            (CASE WHEN COALESCE(p.forename, '') != '' THEN p.forename ELSE r.forename END) AS 'forename',
            (CASE WHEN COALESCE(p.surname, '') != '' THEN p.surname ELSE r.forename END) AS 'surname',
            (CASE WHEN p.dateofbirth IS NOT NULL THEN p.dateofbirth ELSE r.dateofbirth END) AS 'date_of_birth',
            (CASE WHEN COALESCE(p.sex, '') != '' THEN p.sex ELSE r.sex END) AS 'sex',
            (CASE WHEN COALESCE(p.ethnicGp, '') != '' THEN p.ethnicGp ELSE r.ethnicGp END) AS 'ethnic_group',
            (CASE WHEN COALESCE(p.telephone1, '') != '' THEN p.telephone1 ELSE r.telephone1 END) AS 'telephone1',
            (CASE WHEN COALESCE(p.mobile, '') != '' THEN p.mobile ELSE r.mobile END) AS 'mobile',
            (CASE WHEN COALESCE(p.address1, '') != '' OR COALESCE(p.postcode, '') != '' THEN p.address1 ELSE r.address1 END) AS 'address1',
            (CASE WHEN COALESCE(p.address1, '') != '' OR COALESCE(p.postcode, '') != '' THEN p.address2 ELSE r.address2 END) AS 'address2',
            (CASE WHEN COALESCE(p.address1, '') != '' OR COALESCE(p.postcode, '') != '' THEN p.address3 ELSE r.address3 END) AS 'address3',
            (CASE WHEN COALESCE(p.address1, '') != '' OR COALESCE(p.postcode, '') != '' THEN p.postcode ELSE r.postcode END) AS 'postcode'
        FROM patient AS p
        JOIN (
            SELECT
                *
            FROM patient
            WHERE patient.radarNo IS NOT NULL AND patient.sourceType = 'RADAR'
        ) AS r ON p.nhsno = r.nhsno
        LEFT JOIN (
            SELECT
                nhsno,
                unitcode,
                max(date) as load_date
            FROM log
            WHERE action = 'patient data load'
            GROUP BY nhsno, unitcode
        ) AS l ON (p.nhsno = l.nhsno and p.unitcode = l.unitcode)
        LEFT JOIN user ON r.radarConsentConfirmedByUserId = user.id
        ORDER BY
            p.nhsno,
            (CASE WHEN p.sourceType = 'PatientView' THEN 0 ELSE 1 END), -- prefer PatientView patients
            l.load_date DESC -- newer data first
    """))

    seen_nhs_nos = set()
    seen_hospital_nos = set()

    for row in rows:
        nhs_no = row['nhs_no']

        # Use the first patient row for each nhsno
        if nhs_no in seen_nhs_nos:
            continue
        else:
            seen_nhs_nos.add(nhs_no)

        radar_no = row['radar_no']

        # Create a patient
        new_conn.execute(
            tables.patients.insert(),
            id=radar_no,
            created_user_id=migration.user_id,
            modified_user_id=migration.user_id,
        )

        organisation_id = migration.get_organisation_id('UNIT', row['unit_code'])
        recruited_date = row['date_registered']

        username = row['username']

        if username:
            user_id = migration.get_user_id(username)
        else:
            user_id = migration.user_id

        # Add the patient to the RaDaR cohort
        new_conn.execute(
            tables.cohort_patients.insert(),
            cohort_id=migration.cohort_id,
            patient_id=radar_no,
            recruited_organisation_id=organisation_id,
            created_user_id=user_id,
            modified_user_id=user_id,
            created_date=recruited_date,
            modified_date=recruited_date,
        )

        # Add RaDaR demographics
        new_conn.execute(
            tables.patient_demographics.insert(),
            patient_id=radar_no,
            data_source_id=migration.data_source_id,
            first_name=row['forename'],
            last_name=row['surname'],
            date_of_birth=row['date_of_birth'],
            gender=convert_gender(row['sex']),
            ethnicity=convert_ethnicity(row['ethnic_group']),
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
                patient_id=radar_no,
                data_source_id=migration.data_source_id,
                address1=row['address1'],
                address2=row['address2'],
                address3=row['address3'],
                postcode=row['postcode'],
                created_user_id=migration.user_id,
                modified_user_id=migration.user_id,
            )

        hospital_no = row['hospital_number']

        # Note: if a hospital number is duplicated it will be assigned to the first patient (ordered by NHS no)
        if hospital_no and hospital_no not in seen_hospital_nos:
            # Add the patient's hospital number
            new_conn.execute(
                tables.patient_numbers.insert(),
                patient_id=radar_no,
                data_source_id=migration.data_source_id,
                organisation_id=organisation_id,
                number=hospital_no,
                created_user_id=migration.user_id,
                modified_user_id=migration.user_id,
            )

            seen_hospital_nos.add(hospital_no)

        # Note: NHS, CHI, H&C... numbers are all stored in the nhsno column
        organisation_code = number_to_organisation_code(nhs_no)

        if organisation_code is not None:
            new_conn.execute(
                tables.patient_numbers.insert(),
                patient_id=radar_no,
                data_source_id=migration.data_source_id,
                organisation_id=migration.get_organisation_id('OTHER', organisation_code),
                number=nhs_no,
                created_user_id=migration.user_id,
                modified_user_id=migration.user_id,
            )
