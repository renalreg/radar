from sqlalchemy import select

from radar_migration import tables
from radar_migration.patients import migrate_patients
from radar_migration.users import migrate_users, create_migration_user

__version__ = '0.1.0'


class Migration(object):
    def __init__(self, conn):
        self.conn = conn
        self._user_id = None
        self._data_source_id = None
        self._cohort_id = None
        self._organisation_ids = {}

    @property
    def user_id(self):
        if self._user_id is None:
            results = self.conn.execute(select([tables.users.c.id]).where(tables.users.c.username == 'migration'))
            row = results.fetchone()
            user_id = row[0]
            self._user_id = user_id

        return self._user_id

    @property
    def data_source_id(self):
        if self._data_source_id is None:
            s = select([tables.data_sources.c.id])\
                .select_from(tables.data_sources.join(tables.organisations))\
                .where(tables.data_sources.c.type == 'RADAR')\
                .where(tables.organisations.c.code == 'RADAR')
            results = self.conn.execute(s)
            row = results.fetchone()
            self._data_source_id = row[0]

        return self._data_source_id

    @property
    def cohort_id(self):
        if self._cohort_id is None:
            s = select([tables.cohorts.c.id])\
                .where(tables.cohorts.c.code == 'RADAR')
            results = self.conn.execute(s)
            row = results.fetchone()
            self._cohort_id = row[0]

        return self._data_source_id

    def get_organisation_id(self, type, code):
        key = (type, code)
        organisation_id = self._organisation_ids.get(key)

        if organisation_id is None:
            results = self.conn.execute(select([tables.organisations.c.id]).where(tables.organisations.c.code == code))
            row = results.fetchone()
            organisation_id = row[0]
            self._organisation_ids[key] = organisation_id

        return organisation_id


def create_radar(conn):
    result = conn.execute(
        tables.organisations.insert(),
        code='RADAR',
        type='RADAR',
        name='RaDaR',
        recruitment=True,
    )

    organisation_id = result.inserted_primary_key[0]

    conn.execute(
        tables.data_sources.insert(),
        organisation_id=organisation_id,
        type='RADAR',
    )

    conn.execute(
        tables.cohorts.insert(),
        code='RADAR',
        name='RaDaR',
        short_name='RaDaR',
    )


def migrate(old_engine, new_engine):
    old_conn = old_engine.connect()
    new_conn = new_engine.connect()

    create_migration_user(new_conn)
    create_radar(new_conn)

    m = Migration(new_conn)

    migrate_users(m, old_conn, new_conn)
    migrate_patients(m, old_conn, new_conn)
