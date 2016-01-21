from datetime import datetime

from sqlalchemy import select
import pytz

from radar_migration import tables

__version__ = '0.1.0'

EXCLUDED_UNITS = "('RENALREG', 'DEMO', 'BANGALORE', 'CAIRO', 'GUNMA', 'NEWDEHLI', 'TEHRAN', 'VELLORE')"


class ObservationNotFound(Exception):
    pass


class GroupNotFound(Exception):
    pass


class UserNotFound(Exception):
    pass


class DiagnosisNotFound(Exception):
    pass


class DrugNotFound(Exception):
    pass


OBSERVATION_PV_CODE = 0
OBSERVATION_SHORT_NAME = 1


class Migration(object):
    def __init__(self, conn):
        self.conn = conn

        self._user_ids = {}
        self._group_ids = {}
        self._observation_ids = {}
        self._diagnosis_ids = {}
        self._drug_ids = {}
        self._primary_group_ids = {}

        self.now = datetime.now(pytz.UTC)

    @property
    def user_id(self):
        return self.get_user_id('migration')

    @property
    def group_id(self):
        return self.get_group_id('OTHER', 'RADAR')

    @property
    def radar_source_type(self):
        return 'RADAR'

    @property
    def ukrdc_source_type(self):
        return 'UKRDC'

    def get_group_id(self, group_type, group_code):
        group_type = group_type.upper()
        group_code = group_code.upper()

        key = (group_type, group_code)
        group_id = self._group_ids.get(key)

        if group_id is None:
            q = select([tables.groups.c.id])\
                .where(tables.groups.c.type == group_type)\
                .where(tables.groups.c.code == group_code)

            results = self.conn.execute(q)
            row = results.fetchone()

            if row is None:
                group_id = None
            else:
                group_id = row[0]

            self._group_ids[key] = group_id

        if group_id is None:
            raise GroupNotFound('Group not found: %s (%s)' % (group_code, group_type))

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

    def get_observation_id(self, pv_code=None, short_name=None):
        q = select([tables.observations.c.id])

        if pv_code is not None:
            pv_code = pv_code.upper()
            key = (OBSERVATION_PV_CODE, pv_code)
            q = q.where(tables.observations.c.pv_code == pv_code)
        elif short_name is not None:
            key = (OBSERVATION_SHORT_NAME, short_name)
            q = q.where(tables.observations.c.short_name == short_name)
        else:
            raise ValueError('Must supply a pv_code or shortname')

        observation_id = self._observation_ids.get(key)

        if observation_id is None:
            results = self.conn.execute(q)
            row = results.fetchone()

            if row is None:
                observation_id = None
            else:
                observation_id = row[0]

            self._observation_ids[key] = observation_id

        if observation_id is None:
            raise ObservationNotFound('Observation not found: %s' % key[1])

        return observation_id

    def get_diagnosis_id(self, name):
        diagnosis_id = self._diagnosis_ids.get(name)

        if diagnosis_id is None:
            results = self.conn.execute(select([tables.diagnoses.c.id]).where(tables.diagnoses.c.name == name))
            row = results.fetchone()

            if row is None:
                diagnosis_id = None
            else:
                diagnosis_id = row[0]

            self._diagnosis_ids[name] = diagnosis_id

        if diagnosis_id is None:
            raise DiagnosisNotFound('Diagnosis not found: %s' % name)

        return diagnosis_id

    def get_drug_id(self, name):
        drug_id = self._drug_ids.get(name)

        if drug_id is None:
            results = self.conn.execute(select([tables.drugs.c.id]).where(tables.drugs.c.name == name))
            row = results.fetchone()

            if row is None:
                drug_id = None
            else:
                drug_id = row[0]

            self._drug_ids[name] = drug_id

        if drug_id is None:
            raise DrugNotFound('Drug not found: %s' % name)

        return drug_id

    def get_primary_cohort_id(self, patient_id):
        return self.get_primary_group_id('COHORT', patient_id)

    def get_primary_hospital_id(self, patient_id):
        return self.get_primary_group_id('HOSPITAL', patient_id)

    def get_primary_group_id(self, group_type, patient_id):
        key = (group_type, patient_id)
        group_id = self._primary_group_ids.get(patient_id)

        if group_id is None:
            q = select([tables.groups.c.id])
            q = q.select_from(tables.groups.join(tables.group_patients, tables.groups.id == tables.group_patients.c.group_id))
            q = q.where(tables.group.c.type == group_type)
            q = q.where(tables.group_patients.c.patient_id == patient_id)
            q = q.order_by(tables.group_patients.c.id)
            q = q.limit(1)

            print q

            results = self.conn.execute(q)
            row = results.fetchone()

            if row is None:
                group_id = None
            else:
                group_id = row[0]

            self._primary_group_ids[key] = group_id

        if group_id is None:
            raise GroupNotFound('Primary group not found: %s (%s)' % (patient_id, group_type))

        return group_id

    def get_recruited_group_id(self, patient_id):
        group_id = self._recruited_group_ids.get(patient_id)

        if group_id is None:
            q = select([tables.groups.c.id])
            q = q.select_from(tables.groups.join(tables.group_patients, tables.groups.id == tables.group_patients.c.group_id))
            q = q.where(tables.group.c.code == 'RADAR')
            q = q.where(tables.group.c.type == 'OTHER')
            q = q.where(tables.group_patients.c.patient_id == patient_id)
            q = q.order_by(tables.group_patients.c.from_date)
            q = q.limit(1)

            print q

            results = self.conn.execute(q)
            row = results.fetchone()

            if row is None:
                group_id = None
            else:
                group_id = row[0]

            self._recruited_group_ids[patient_id] = group_id

        if group_id is None:
            raise GroupNotFound('Recruited group not found: %s' % patient_id)

        return group_id


def check_patient_exists(conn, patient_id):
    q = select().where(tables.patients.c.id == patient_id)
    return conn.execute(q).fetchone() is not None


def bit_to_bool(value):
    if value is None:
        r = None
    elif value == '\0':
        r = False
    elif value == '\1':
        r = True
    else:
        raise ValueError('Not a bit')

    return r


def int_to_bool(value):
    if value is None:
        r = None
    elif value == 0:
        r = False
    elif value == 1:
        r = True
    else:
        raise ValueError('Not 0 or 1')

    return r
