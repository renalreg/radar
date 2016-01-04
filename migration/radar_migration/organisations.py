import csv

from sqlalchemy import text

from radar_migration import tables


def create_organisation(conn, code, type, name, recruitment):
    result = conn.execute(
        tables.organisations.insert(),
        code=code,
        type=type,
        name=name,
        recruitment=recruitment,
    )

    organisation_id = result.inserted_primary_key[0]

    return organisation_id


def create_organisations(conn, filename):
    with open(filename, 'rb') as f:
        reader = csv.reader(f)

        for code, name, recruitment in reader:
            recruitment = recruitment == '1'

            create_organisation(
                conn,
                code=code,
                type='OTHER',
                name=name,
                recruitment=recruitment,
            )


def create_units(conn, filename):
    with open(filename, 'rb') as f:
        reader = csv.reader(f)

        for code, name in reader:
            create_organisation(
                conn,
                code=code,
                type='UNIT',
                name=name,
                recruitment=False
            )


def migrate_patient_organisations(m, old_conn, new_conn):
    rows = old_conn.execute(text("""
        SELECT DISTINCT
            patient.radarNo,
            unit.unitcode
        FROM usermapping
        JOIN patient ON usermapping.nhsno = patient.nhsno
        JOIN unit ON usermapping.unitcode = unit.unitcode
        WHERE
            patient.radarNo IS NOT NULL AND
            patient.sourceType = 'RADAR' AND
            unit.sourceType = 'renalunit'
    """))

    for radar_no, unit_code in rows:
        organisation_id = m.get_organisation_id('UNIT', unit_code)

        new_conn.execute(
            tables.organisation_patients.insert(),
            patient_id=radar_no,
            organisation_id=organisation_id,
            created_user_id=m.user_id,
            modified_user_id=m.user_id,
        )


def migrate_user_organisations(m, old_conn, new_conn):
    rows = old_conn.execute(text("""
        SELECT
            user.username,
            unit.unitcode,
            rdr_user_mapping.role
        FROM usermapping
        JOIN user ON usermapping.username = user.username
        JOIN unit ON usermapping.unitcode = unit.unitcode
        JOIN rdr_user_mapping ON user.id = rdr_user_mapping.userId
        WHERE
            usermapping.unitcode != 'RENALREG' AND
            usermapping.unitcode != 'DEMO' AND
            usermapping.unitcode != 'UNKNOWN' AND
            unit.sourceType = 'renalunit' AND
            rdr_user_mapping.role != 'ROLE_PATIENT'
    """))

    for username, unit_code, role in rows:
        print username, unit_code, role
