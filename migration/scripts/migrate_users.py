from sqlalchemy import create_engine, text
import click

from radar_migration import tables, Migration
from radar_migration.cohorts import convert_cohort_code


def migrate_users(old_conn, new_conn):
    # Exclude patient users
    rows = old_conn.execute(text("""
        SELECT
            username,
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

        print 'user %s' % username

        is_admin = row['role'] == 'ROLE_SUPER_USER'

        new_conn.execute(
            tables.users.insert(),
            username=username,
            email=row['email'],
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
            tables.cohort_users.insert(),
            cohort_id=cohort_id,
            user_id=user_id,
            role='RESEARCHER',
            created_user_id=m.user_id,
            modified_user_id=m.user_id,
        )


def migrate_user_organisations(old_conn, new_conn):
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
            usermapping.unitcode != 'RENALREG' AND
            usermapping.unitcode != 'DEMO' AND
            usermapping.unitcode != 'UNKNOWN' AND
            unit.sourceType = 'renalunit' AND
            rdr_user_mapping.role != 'ROLE_PATIENT'
    """))

    for username, unit_code in rows:
        organisation_id = m.get_organisation_id('UNIT', unit_code)
        user_id = m.get_user_id(username)

        new_conn.execute(
            tables.organisation_users.insert(),
            organisation_id=organisation_id,
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
        migrate_user_organisations(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
