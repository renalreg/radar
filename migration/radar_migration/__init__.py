from sqlalchemy import select

from radar_migration import tables

__version__ = '0.1.0'


class MigrationError(Exception):
    pass


class Migration(object):
    def __init__(self, conn):
        self.conn = conn

        self._data_source_id = None

        self._user_ids = {}
        self._organisation_ids = {}
        self._cohort_ids = {}

    @property
    def user_id(self):
        return self.get_user_id('migration')

    @property
    def organisation_id(self):
        return self.get_organisation_id('OTHER', 'RADAR')

    @property
    def data_source_id(self):
        if self._data_source_id is None:
            s = select([tables.data_sources.c.id])\
                .where(tables.data_sources.c.organisation_id == self.organisation_id)\
                .where(tables.data_sources.c.type == 'RADAR')
            results = self.conn.execute(s)
            row = results.fetchone()

            if row is None:
                raise MigrationError('Data source not found')

            self._data_source_id = row[0]

        return self._data_source_id

    @property
    def cohort_id(self):
        return self.get_cohort_id('RADAR')

    def get_organisation_id(self, type, code):
        key = (type, code)
        organisation_id = self._organisation_ids.get(key)

        if organisation_id is None:
            q = select([tables.organisations.c.id])\
                .where(tables.organisations.c.type == type)\
                .where(tables.organisations.c.code == code)

            results = self.conn.execute(q)
            row = results.fetchone()

            if row is None:
                raise MigrationError('Organisation not found: %s (%s)' % (code, type))

            organisation_id = row[0]
            self._organisation_ids[key] = organisation_id

        return organisation_id

    def get_cohort_id(self, code):
        key = (type, code)
        cohort_id = self._cohort_ids.get(key)

        if cohort_id is None:
            results = self.conn.execute(select([tables.cohorts.c.id]).where(tables.cohorts.c.code == code))
            row = results.fetchone()

            if row is None:
                raise MigrationError('Cohort not found: %s' % code)

            cohort_id = row[0]
            self._cohort_ids[key] = cohort_id

        return cohort_id

    def get_user_id(self, username):
        user_id = self._user_ids.get(username)

        if user_id is None:
            results = self.conn.execute(select([tables.users.c.id]).where(tables.users.c.username == username))
            row = results.fetchone()

            if row is None:
                raise MigrationError('User not found: %s' % username)

            user_id = row[0]
            self._user_ids[username] = user_id

        return user_id
