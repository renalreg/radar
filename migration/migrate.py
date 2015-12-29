from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, MetaData, String, ForeignKey, Date
from sqlalchemy.sql import select
import click

metadata = MetaData()

patients = Table(
    'patients', metadata,
    Column('id', Integer, primary_key=True),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String),
    Column('first_name', String),
    Column('last_name', String),
    Column('email', String),
)

patient_demographics = Table(
    'patient_demographics', metadata,
    Column('patient_id', Integer),
    Column('data_source_id', Integer),
    Column('first_name', String),
    Column('last_name', String),
    Column('date_of_birth', Date),
    Column('gender', Integer),
    Column('ethnicity', String),
    Column('home_number', String),
    Column('mobile_number', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

patient_addresses = Table(
    'patient_addresses', metadata,
    Column('patient_id', Integer),
    Column('data_source_id', Integer),
    Column('address1', String),
    Column('address2', String),
    Column('address3', Integer),
    Column('postcode', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

organisations = Table(
    'organisations', metadata,
    Column('id', Integer),
    Column('code', String),
)

data_sources = Table(
    'data_sources', metadata,
    Column('id', Integer),
    Column('organisation_id', Integer, ForeignKey('organisations.id')),
    Column('type', String),
)


class Migration(object):
    def __init__(self):
        self.conn = None
        self._user_id = None
        self._data_source_id = None
        self._organisation_ids = {}

    def bind(self, conn):
        self.conn = conn

    @property
    def user_id(self):
        if self._user_id is None:
            result = self.conn.execute(users.insert(), username='migration')
            self._user_id = result.inserted_primary_key[0]

        return self._user_id

    @property
    def data_source_id(self):
        if self._data_source_id is None:
            s = select([data_sources.c.id])\
                .select_from(data_sources.join(organisations))\
                .where(data_sources.c.type == 'RADAR')\
                .where(organisations.c.code == 'RADAR')
            results = self.conn.execute(s)
            row = results.fetchone()
            self._data_source_id = row[0]

        return self._data_source_id

    def get_organisation_id(self, code):
        organisation_id = self._organisation_ids.get(code)

        if organisation_id is None:
            results = self.conn.execute(select([organisations.c.id]).where(users.c.code == code))
            row = results.fetchone()
            organisation_id = row[0]
            self._organisation_ids[code] = organisation_id

        return organisation_id

migration = Migration()

ETHNICITY_MAP = {
    '9S1..': 'A',
    '9S2..': 'M',
    '9S3..': 'N',
    '9S4..': 'P',
    '9S41.': 'P',
    '9S42.': 'M',
    '9S43.': 'N',
    '9S44.': 'N',
    '9S45.': 'P',
    '9S46.': 'P',
    '9S47.': 'P',
    '9S48.': 'P',
    '9S5..': 'P',
    '9S51.': 'P',
    '9S52.': 'P',
    '9S6..': 'H',
    '9S7..': 'J',
    '9S8..': 'K',
    '9S9..': 'R',
    '9SA..': 'S',
    '9SA1.': 'S',
    '9SA3.': 'M',
    '9SA4.': 'S',
    '9SA5.': 'S',
    '9SA6.': 'L',
    '9SA7.': 'L',
    '9SA8.': 'L',
    '9SA9.': 'B',
    '9SAA.': 'C',
    '9SAB.': 'C',
    '9SAC.': 'C',
    '9SAD.': 'S',
    '9SB..': 'G',
    '9SB1.': 'E',
    '9SB2.': 'F',
    '9SB3.': 'C',
    '9SB4.': 'G',
}


def convert_ethnicity(old_value):
    if old_value:
        new_value = ETHNICITY_MAP[old_value.upper().ljust(5, '.')]
    else:
        new_value = None

    return new_value


def convert_gender(old_value):
    if old_value in ['M', 'Male']:
        new_value = 1
    elif old_value in ['F', 'Female']:
        new_value = 2
    else:
        new_value = None

    return new_value


def migrate(old_engine, new_engine):
    old_conn = old_engine.connect()
    new_conn = new_engine.connect()
    migration.bind(new_conn)
    migrate_users(old_conn, new_conn)
    migrate_patients(old_conn, new_conn)


def migrate_users(old_conn, new_conn):
    rows = old_conn.execute("""
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
    """)

    for row in rows:
        # Insert into users
        new_conn.execute(
            users.insert(),
            username=row['username'],
            email=row['email'],
            first_name=row['firstName'],
            last_name=row['lastName'],
        )


def migrate_patients(old_conn, new_conn):
    # TODO use latest record
    rows = old_conn.execute("""
        select
            radarNo,
            forename,
            surname,
            sex,
            address1,
            address2,
            address3,
            postcode,
            dateReg,
            telephone1,
            mobile,
            dateofbirth,
            ethnicGp
        from patient
        where radarNo is not null
    """)

    for row in rows:
        patient_id = row['radarNo']

        # Insert into patients
        new_conn.execute(
            patients.insert(),
            id=patient_id,
            created_user_id=migration.user_id,
            modified_user_id=migration.user_id,
        )

        # Insert into patient_demographics
        new_conn.execute(
            patient_demographics.insert(),
            patient_id=patient_id,
            data_source_id=migration.data_source_id,
            first_name=row['forename'],
            last_name=row['surname'],
            date_of_birth=row['dateofbirth'],
            gender=convert_gender(row['sex']),
            ethnicity=convert_ethnicity(row['ethnicGp']),
            home_number=row['telephone1'],
            mobile_number=row['mobile'],
            created_user_id=migration.user_id,
            modified_user_id=migration.user_id,
        )

        if any(row[x] for x in ['address1', 'address2', 'address3', 'postcode']):
            # Insert into patient_addresses
            new_conn.execute(
                patient_addresses.insert(),
                patient_id=patient_id,
                data_source_id=migration.data_source_id,
                address1=row['address1'],
                address2=row['address2'],
                address3=row['address3'],
                postcode=row['postcode'],
                created_user_id=migration.user_id,
                modified_user_id=migration.user_id,
            )

        # TODO dateReg, unitcode, hospitalnumber, nhsno/nhsNoType


@click.command()
@click.option('--old-connection-string', default='mysql+pymysql://dbaccess@localhost:3306/patientview')
@click.option('--new-connection-string', default='postgresql+psycopg2://postgres:password@localhost:5432/radar')
def cli(old_connection_string, new_connection_string):
    old_engine = create_engine(old_connection_string, echo=True)
    new_engine = create_engine(new_connection_string, echo=True)
    migrate(old_engine, new_engine)


if __name__ == '__main__':
    cli()
