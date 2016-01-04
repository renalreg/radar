import csv

from sqlalchemy import text

from radar_migration import tables


def create_cohort(conn, code, name, short_name, features):
    result = conn.execute(
        tables.cohorts.insert(),
        code=code,
        name=name,
        short_name=short_name,
    )

    cohort_id = result.inserted_primary_key[0]

    for i, feature in enumerate(features):
        # Leave gaps between features
        weight = i * 100

        conn.execute(
            tables.cohort_features.insert(),
            cohort_id=cohort_id,
            name=name,
            weight=weight,
        )


def create_cohorts(conn, filename):
    with open(filename, 'rb') as f:
        reader = csv.reader(f)

        for code, name, short_name, features in reader:
            features = features.split(',')

            create_cohort(
                conn,
                code=code,
                name=name,
                short_name=short_name,
                features=features,
            )


def migrate_patient_cohorts(m, old_conn, new_conn):
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
            unit.sourceType = 'radargroup'
    """))

    for radar_no, cohort_code in rows:
        cohort_id = m.get_cohort_id(cohort_code)

        new_conn.execute(
            tables.cohort_patients.insert(),
            patient_id=radar_no,
            cohort_id=cohort_id,
            recruitment_organisation_id=m.organisation_id,
            created_user_id=m.user_id,
            modified_user_id=m.user_id,
        )


def migrate_user_cohorts(m, old_conn, new_conn):
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
            unit.sourceType = 'radargroup' AND
            rdr_user_mapping.role != 'ROLE_PATIENT'
    """))

    for username, cohort_code, role in rows:
        print username, cohort_code, role
