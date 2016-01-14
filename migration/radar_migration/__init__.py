from sqlalchemy import select

from radar_migration import tables

__version__ = '0.1.0'

EXCLUDED_UNITS = "('RENALREG', 'DEMO', 'BANGALORE', 'CAIRO', 'GUNMA', 'NEWDEHLI', 'TEHRAN', 'VELLORE')"


class ObservationNotFound(Exception):
    pass


class GroupNotFound(Exception):
    pass


class UserNotFound(Exception):
    pass


class Migration(object):
    def __init__(self, conn):
        self.conn = conn

        self._user_ids = {}
        self._group_ids = {}
        self._observation_ids = {}

    @property
    def user_id(self):
        return self.get_user_id('migration')

    @property
    def group_id(self):
        return self.get_group_id('OTHER', 'RADAR')

    @property
    def source_type(self):
        return 'RADAR'

    def get_group_id(self, type, code):
        key = (type, code)
        group_id = self._group_ids.get(key)

        if group_id is None:
            q = select([tables.groups.c.id])\
                .where(tables.groups.c.type == type)\
                .where(tables.groups.c.code == code)

            results = self.conn.execute(q)
            row = results.fetchone()

            if row is None:
                group_id = None
            else:
                group_id = row[0]

            self._group_ids[key] = group_id

        if group_id is None:
            raise GroupNotFound('Group not found: %s (%s)' % (code, type))

        return group_id

    def get_cohort_id(self, code):
        return self.get_group_id('COHORT', code)

    def get_hospital_id(self, code):
        return self.get_group_id('HOSPITAL', code)

    def get_user_id(self, username):
        username = username.lower()

        user_id = self._user_ids.get(username)

        if user_id is None:
            results = self.conn.execute(select([tables.users.c.id]).where(tables.users.c.username == username))
            row = results.fetchone()

            if row is None:
                user_id = None
            else:
                user_id = row[0]

            self._user_ids[username] = user_id

        if user_id is None:
            raise UserNotFound('User not found: %s' % username)

        return user_id

    def get_observation_id(self, pv_code):
        pv_code = pv_code.upper()

        observation_id = self._observation_ids.get(pv_code)

        if observation_id is None:
            q = select([tables.observations.c.id])\
                .where(tables.observations.c.value_type == 'REAL')\
                .where(tables.observations.c.pv_code == pv_code)

            results = self.conn.execute(q)
            row = results.fetchone()

            if row is None:
                observation_id = None
            else:
                observation_id = row[0]

            self._observation_ids[pv_code] = observation_id

        if observation_id is None:
            raise ObservationNotFound('Observation not found: %s' % pv_code)

        return observation_id
