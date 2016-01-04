from sqlalchemy import text

from radar_migration import tables


def create_migration_user(conn):
    conn.execute(tables.users.insert(), username='migration')


def migrate_users(m, old_conn, new_conn):
    # Exclude patient users
    rows = old_conn.execute(text("""
        select
            username,
            email,
            firstName,
            lastName
        from user
        join rdr_user_mapping on (user.id = rdr_user_mapping.userId)
        join tbl_users on (rdr_user_mapping.radarUserId = tbl_users.uId)
        where
            rdr_user_mapping.role != 'ROLE_PATIENT'
    """))

    for row in rows:
        # Insert into users
        new_conn.execute(
            tables.users.insert(),
            username=row['username'],
            email=row['email'],
            first_name=row['firstName'],
            last_name=row['lastName'],
        )
