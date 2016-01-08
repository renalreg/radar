from sqlalchemy import text, create_engine
import click

from radar_migration import tables, Migration, EXCLUDED_UNITS
from radar_migration.cohorts import convert_cohort_code


ETHNICITY_MAP = {
    '9S1..': 'A',
    '9S2..': 'M',
    '9S3..': 'N',
    '9S4..': 'P',
    '9S41.': 'P',
    '9S42.': 'M',
    '9S43.': 'N',
    '9S44.': 'N',
    '9S45.': 'P',
    '9S46.': 'P',
    '9S47.': 'P',
    '9S48.': 'P',
    '9S5..': 'P',
    '9S51.': 'P',
    '9S52.': 'P',
    '9S6..': 'H',
    '9S7..': 'J',
    '9S8..': 'K',
    '9S9..': 'R',
    '9SA..': 'S',
    '9SA1.': 'S',
    '9SA3.': 'M',
    '9SA4.': 'S',
    '9SA5.': 'S',
    '9SA6.': 'L',
    '9SA7.': 'L',
    '9SA8.': 'L',
    '9SA9.': 'B',
    '9SAA.': 'C',
    '9SAB.': 'C',
    '9SAC.': 'C',
    '9SAD.': 'S',
    '9SB..': 'G',
    '9SB1.': 'E',
    '9SB2.': 'F',
    '9SB3.': 'C',
    '9SB4.': 'G',
}

STATUS_MAP = {
    None: True,
    0: True,
    1: True,
    2: False,
    3: False,
    4: False,
    5: False,
    6: False,
}


def convert_ethnicity(old_value):
    if old_value:
        try:
            new_value = ETHNICITY_MAP[old_value.upper().ljust(5, '.')]
        except KeyError:
            raise ValueError('Unknown ethnicity: %s' % old_value)
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


def convert_status(old_value):
    try:
        new_value = STATUS_MAP[old_value]
    except KeyError:
        raise ValueError('Unknown status: %s' % old_value)

    return new_value


def number_to_organisation_code(value):
    if len(value) != 10 or not value.isdigit():
        return None
    elif value >= '0101000000' and value <= '3112999999':
        return 'CHI'
    elif value >= '3200000010' and value <= '3999999999':
        return 'HANDC'
    else:
        return 'NHS'


def migrate_patients(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT
            r.radarNo AS 'radar_no',
            r.nhsno AS 'nhs_no',
            r.unitcode AS 'unit_code',
            CAST(LEAST(
                COALESCE(p.dateReg, NOW()),
                COALESCE(rdr_radar_number.creationDate, NOW()),
                COALESCE(d.DATE_REG, NOW())
            ) AS DATE) AS 'date_registered',
            user.username AS 'username',
            (
                CASE
                    WHEN COALESCE(p.forename, '') != '' THEN p.forename
                    WHEN COALESCE(r.forename, '') != '' THEN r.forename
                    ELSE d.FNAME
                END
            ) AS 'forename',
            (
                CASE
                    WHEN COALESCE(p.surname, '') != '' THEN p.surname
                    WHEN COALESCE(r.surname, '') != '' THEN r.surname
                    ELSE d.SNAME
                END
            ) AS 'surname',
            (
                CASE
                    WHEN p.dateofbirth IS NOT NULL THEN p.dateofbirth
                    WHEN r.dateofbirth IS NOT NULL THEN r.dateofbirth
                    ELSE d.DOB
                END
            ) AS 'date_of_birth',
            (
                CASE
                    WHEN COALESCE(p.sex, '') != '' THEN p.sex
                    WHEN COALESCE(r.sex, '') != '' THEN r.sex
                    ELSE d.sex
                END
            ) AS 'sex',
            (
                CASE
                    WHEN COALESCE(p.ethnicGp, '') != '' THEN p.ethnicGp
                    WHEN COALESCE(r.ethnicGp, '') != '' THEN r.ethnicGp
                    ELSE d.ETHNIC_GP
                END
            ) AS 'ethnic_group',
            (
                CASE
                    WHEN COALESCE(p.telephone1, '') != '' THEN p.telephone1
                    WHEN COALESCE(p.telephone2, '') != '' THEN p.telephone2
                    WHEN COALESCE(r.telephone1, '') != '' THEN r.telephone1
                    WHEN COALESCE(r.telephone2, '') != '' THEN r.telephone2
                    WHEN COALESCE(d.phone1, '') != '' THEN d.phone1
                    WHEN COALESCE(d.phone2, '') != '' THEN d.phone2
                    ELSE NULL
                END
            ) AS 'telephone1',
            (
                CASE
                    WHEN COALESCE(p.mobile, '') != '' THEN p.mobile
                    WHEN COALESCE(r.mobile, '') != '' THEN r.mobile
                    WHEN COALESCE(d.mobile, '') NOT IN ('', 'mobile') THEN d.mobile
                    ELSE NULL
                END
            ) AS 'mobile',
            r.comments,
            r.otherClinicianAndContactInfo,
            r.status
        FROM patient AS p
        JOIN (
            SELECT
                *
            FROM patient
            WHERE radarNo IS NOT NULL
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
        LEFT JOIN tbl_demographics AS d ON r.radarNo = d.RADAR_NO
        LEFT JOIN rdr_radar_number ON r.radarNo = rdr_radar_number.id
        WHERE
            r.unitcode NOT IN ('DEMO', 'RENALREG', 'BANGALORE', 'CAIRO', 'GUNMA', 'NEWDEHLI', 'TEHRAN', 'VELLORE')
        ORDER BY
            p.nhsno,
            (CASE WHEN p.sourceType = 'PatientView' THEN 0 ELSE 1 END), -- prefer PatientView patients
            l.load_date DESC -- newer data first
    """))

    seen_nhs_nos = set()

    for row in rows:
        nhs_no = row['nhs_no']

        # Use the first patient row for each nhsno
        if nhs_no in seen_nhs_nos:
            continue
        else:
            seen_nhs_nos.add(nhs_no)

        radar_no = row['radar_no']

        print 'patient %d' % radar_no

        comments = [row['comments'], row['otherClinicianAndContactInfo']]
        comments = [x for x in comments if x]

        if comments:
            comments = '\n'.join(comments)
        else:
            comments = None

        is_active = convert_status(row['status'])

        # Create a patient
        new_conn.execute(
            tables.patients.insert(),
            id=radar_no,
            comments=comments,
            is_active=is_active,
            created_user_id=m.user_id,
            modified_user_id=m.user_id,
        )

        organisation_id = m.get_organisation_id('UNIT', row['unit_code'])
        recruited_date = row['date_registered']

        username = row['username']

        if username:
            user_id = m.get_user_id(username)
        else:
            user_id = m.user_id

        # Add the patient to the RaDaR cohort
        new_conn.execute(
            tables.cohort_patients.insert(),
            cohort_id=m.cohort_id,
            patient_id=radar_no,
            recruited_organisation_id=organisation_id,
            created_user_id=user_id,
            modified_user_id=user_id,
            created_date=recruited_date,
            modified_date=recruited_date,
        )

        first_name = row['forename'].upper()
        last_name = row['surname'].upper()

        # Add RaDaR demographics
        new_conn.execute(
            tables.patient_demographics.insert(),
            patient_id=radar_no,
            data_source_id=m.data_source_id,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=row['date_of_birth'],
            gender=convert_gender(row['sex']),
            ethnicity=convert_ethnicity(row['ethnic_group']),
            home_number=row['telephone1'],
            mobile_number=row['mobile'],
            created_user_id=m.user_id,
            modified_user_id=m.user_id,
        )

        # Note: NHS, CHI, H&C... numbers are all stored in the nhsno column
        organisation_code = number_to_organisation_code(nhs_no)

        if organisation_code is not None:
            new_conn.execute(
                tables.patient_numbers.insert(),
                patient_id=radar_no,
                data_source_id=m.data_source_id,
                organisation_id=m.get_organisation_id('OTHER', organisation_code),
                number=nhs_no,
                created_user_id=m.user_id,
                modified_user_id=m.user_id,
            )


def migrate_patient_cohorts(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT DISTINCT
            patient.radarNo,
            unit.unitcode,
            CAST(LEAST(
                COALESCE(patient.dateReg, NOW()),
                COALESCE(rdr_radar_number.creationDate, NOW()),
                COALESCE(tbl_demographics.DATE_REG, NOW())
            ) AS DATE) AS dateReg
        FROM usermapping
        JOIN patient ON usermapping.nhsno = patient.nhsno
        JOIN unit ON usermapping.unitcode = unit.unitcode
        LEFT JOIN rdr_radar_number ON patient.radarNo = rdr_radar_number.id
        LEFT JOIN tbl_demographics ON patient.radarNo = tbl_demographics.radar_no
        WHERE
            patient.radarNo IS NOT NULL AND
            patient.unitcode NOT IN %s AND
            unit.sourceType = 'radargroup'
    """ % EXCLUDED_UNITS))

    for row in rows:
        cohort_code = convert_cohort_code(row['unitcode'])
        cohort_id = m.get_cohort_id(cohort_code)

        new_conn.execute(
            tables.cohort_patients.insert(),
            patient_id=row['radarNo'],
            cohort_id=cohort_id,
            recruited_organisation_id=m.organisation_id,
            created_user_id=m.user_id,
            modified_user_id=m.user_id,
            created_date=row['dateReg'],
            modified_date=row['dateReg'],
        )


def migrate_patient_organisations(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT DISTINCT
            patient.radarNo,
            unit.unitcode,
            CAST(LEAST(
                COALESCE(patient.dateReg, NOW()),
                COALESCE(rdr_radar_number.creationDate, NOW()),
                COALESCE(tbl_demographics.DATE_REG, NOW())
            ) AS DATE) AS dateReg
        FROM usermapping
        JOIN patient ON usermapping.nhsno = patient.nhsno
        JOIN unit ON usermapping.unitcode = unit.unitcode
        LEFT JOIN rdr_radar_number ON patient.radarNo = rdr_radar_number.id
        LEFT JOIN tbl_demographics ON patient.radarNo = tbl_demographics.radar_no
        WHERE
            patient.radarNo IS NOT NULL AND
            patient.unitcode NOT IN %s AND
            usermapping.unitcode NOT IN (
                'RENALREG', 'DEMO', 'UNKNOWN', 'DUMMY',
                'CHI', 'CCL', 'ECS',
                'BANGALORE', 'CAIRO', 'GUNMA', 'NEWDEHLI', 'TEHRAN', 'VELLORE'
            ) AND
            unit.sourceType = 'renalunit'
    """ % EXCLUDED_UNITS))

    for row in rows:
        organisation_id = m.get_organisation_id('UNIT', row['unitcode'])

        new_conn.execute(
            tables.organisation_patients.insert(),
            patient_id=row['radarNo'],
            organisation_id=organisation_id,
            created_user_id=m.user_id,
            modified_user_id=m.user_id,
            created_date=row['dateReg'],
            modified_date=row['dateReg'],
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
        migrate_patients(src_conn, dest_conn)
        migrate_patient_cohorts(src_conn, dest_conn)
        migrate_patient_organisations(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
