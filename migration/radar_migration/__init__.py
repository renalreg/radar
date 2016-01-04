from sqlalchemy import select

from radar_migration import tables
from radar_migration.patients import migrate_patients
from radar_migration.users import migrate_users, create_migration_user
from radar_migration.organisations import create_organisations, create_units,\
    migrate_patient_organisations, create_organisation
from radar_migration.cohorts import migrate_patient_cohorts, create_cohort,\
    create_cohorts

__version__ = '0.1.0'


class Migration(object):
    def __init__(self, conn):
        self.conn = conn

        self._user_id = None
        self._user_ids = {}

        self._data_source_id = None

        self._organisation_id = None
        self._organisation_ids = {}

        self._cohort_id = None
        self._cohort_ids = {}

    @property
    def user_id(self):
        if self._user_id is None:
            results = self.conn.execute(select([tables.users.c.id]).where(tables.users.c.username == 'migration'))
            row = results.fetchone()
            user_id = row[0]
            self._user_id = user_id

        return self._user_id

    @property
    def organisation_id(self):
        if self._organisation_id is None:
            s = select([tables.organisations.c.id])\
                .where(tables.organisations.c.type == 'OTHER')\
                .where(tables.organisations.c.code == 'RADAR')
            results = self.conn.execute(s)
            row = results.fetchone()
            self._organisation_id = row[0]

        return self._organisation_id

    @property
    def data_source_id(self):
        if self._data_source_id is None:
            s = select([tables.data_sources.c.id])\
                .where(tables.data_sources.c.organisation_id == self.organisation_id)\
                .where(tables.data_sources.c.type == 'RADAR')
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

        return self._cohort_id

    def get_organisation_id(self, type, code):
        key = (type, code)
        organisation_id = self._organisation_ids.get(key)

        if organisation_id is None:
            results = self.conn.execute(select([tables.organisations.c.id]).where(tables.organisations.c.code == code))
            row = results.fetchone()
            organisation_id = row[0]
            self._organisation_ids[key] = organisation_id

        return organisation_id

    def get_cohort_id(self, code):
        key = (type, code)
        cohort_id = self._cohort_ids.get(key)

        if cohort_id is None:
            results = self.conn.execute(select([tables.cohorts.c.id]).where(tables.cohorts.c.code == code))
            row = results.fetchone()
            cohort_id = row[0]
            self._cohort_ids[key] = cohort_id

        return cohort_id

    def get_user_id(self, username):
        user_id = self._user_ids.get(username)

        if user_id is None:
            results = self.conn.execute(select([tables.users.c.id]).where(tables.users.c.username == username))
            row = results.fetchone()
            user_id = row[0]
            self._user_ids[username] = user_id

        return user_id


def create_radar(conn):
    organisation_id = create_organisation(
        conn,
        code='RADAR',
        type='OTHER',
        name='RaDaR',
        recruitment=True,
    )

    conn.execute(
        tables.data_sources.insert(),
        organisation_id=organisation_id,
        type='RADAR',
    )

    create_cohort(
        conn,
        code='RADAR',
        name='RaDaR',
        short_name='RaDaR',
        features=['DEMOGRAPHICS', 'CONSULTANTS', 'COHORTS', 'UNITS']
    )


def migrate(
    old_engine,
    new_engine,
    units_filename='units.csv',
    organisations_filename='organisations.csv',
    cohorts_filename='cohorts.csv'
):
    old_conn = old_engine.connect()
    new_conn = new_engine.connect()

    create_migration_user(new_conn)
    create_radar(new_conn)
    create_units(new_conn, units_filename)
    create_organisations(new_conn, organisations_filename)
    create_cohorts(new_conn, cohorts_filename)

    m = Migration(new_conn)

    migrate_users(m, old_conn, new_conn)
    migrate_patients(m, old_conn, new_conn)
    migrate_patient_organisations(m, old_conn, new_conn)
    migrate_patient_cohorts(m, old_conn, new_conn)
