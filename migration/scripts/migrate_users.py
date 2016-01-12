from sqlalchemy import create_engine, text
import click

from radar_migration import tables, Migration
from radar_migration.groups import convert_cohort_code


def migrate_users(old_conn, new_conn):
    # Exclude patient users
    rows = old_conn.execute(text("""
        SELECT
            username,
            password,
            email,
            firstName,
            lastName,
            role
        FROM user
        JOIN rdr_user_mapping ON user.id = rdr_user_mapping.userId
        JOIN tbl_users ON rdr_user_mapping.radarUserId = tbl_users.uId
        WHERE
            rdr_user_mapping.role != 'ROLE_PATIENT'
        ORDER BY username
    """))

    for row in rows:
        username = row['username'].lower()
        email = row['email'].lower()
        password_hash = 'sha256$$' + row['password']

        print 'user %s' % username

        is_admin = row['role'] == 'ROLE_SUPER_USER'

        new_conn.execute(
            tables.users.insert(),
            username=username,
            password_hash=password_hash,
            email=email,
            first_name=row['firstName'],
            last_name=row['lastName'],
            is_admin=is_admin,
        )


def migrate_user_cohorts(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT DISTINCT
            user.username,
            unit.unitcode
        FROM usermapping
        JOIN user ON usermapping.username = user.username
        JOIN unit ON usermapping.unitcode = unit.unitcode
        JOIN rdr_user_mapping ON user.id = rdr_user_mapping.userId
        JOIN tbl_users ON rdr_user_mapping.radarUserId = tbl_users.uId
        WHERE
            unit.sourceType = 'radargroup' AND
            rdr_user_mapping.role != 'ROLE_PATIENT'
    """))

    for username, cohort_code in rows:
        cohort_code = convert_cohort_code(cohort_code)
        cohort_id = m.get_cohort_id(cohort_code)
        user_id = m.get_user_id(username)

        new_conn.execute(
            tables.group_users.insert(),
            group_id=cohort_id,
            user_id=user_id,
            role='RESEARCHER',
            created_user_id=m.user_id,
            modified_user_id=m.user_id,
        )


def migrate_user_hospitals(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT DISTINCT
            user.username,
            unit.unitcode
        FROM usermapping
        JOIN user ON usermapping.username = user.username
        JOIN unit ON usermapping.unitcode = unit.unitcode
        JOIN rdr_user_mapping ON user.id = rdr_user_mapping.userId
        JOIN tbl_users ON rdr_user_mapping.radarUserId = tbl_users.uId
        WHERE
            usermapping.unitcode NOT IN (
                'RENALREG', 'DEMO', 'UNKNOWN', 'DUMMY',
                'CHI', 'CCL', 'ECS',
                'BANGALORE', 'CAIRO', 'GUNMA', 'NEWDEHLI', 'TEHRAN', 'VELLORE'
            ) AND
            unit.sourceType = 'renalunit' AND
            rdr_user_mapping.role != 'ROLE_PATIENT'
    """))

    for username, hospital_code in rows:
        hospital_id = m.get_hospital_id(hospital_code)
        user_id = m.get_user_id(username)

        new_conn.execute(
            tables.group_users.insert(),
            group_id=hospital_id,
            user_id=user_id,
            role='CLINICIAN',
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
        migrate_users(src_conn, dest_conn)
        migrate_user_cohorts(src_conn, dest_conn)
        migrate_user_hospitals(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
