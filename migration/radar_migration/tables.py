from sqlalchemy import MetaData, Table, Column, Integer, String, Date, ForeignKey,\
    DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

patients = Table(
    'patients', metadata,
    Column('id', Integer, primary_key=True),
    Column('comments', String),
    Column('is_active', Boolean),
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
    Column('is_admin', Boolean),
)

cohorts = Table(
    'cohorts', metadata,
    Column('id', Integer, primary_key=True),
    Column('code', String, primary_key=True),
    Column('name', String),
    Column('short_name', String),
)

cohort_features = Table(
    'cohort_features', metadata,
    Column('id', Integer, primary_key=True),
    Column('patient_id', Integer),
    Column('name', String),
    Column('weight', Integer),
)

cohort_patients = Table(
    'cohort_patients', metadata,
    Column('id', Integer, primary_key=True),
    Column('cohort_id', Integer),
    Column('patient_id', Integer),
    Column('recruited_organisation_id', Integer),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
    Column('created_date', DateTime),
    Column('modified_date', DateTime),
)

cohort_users = Table(
    'cohort_users', metadata,
    Column('id', Integer, primary_key=True),
    Column('cohort_id', Integer),
    Column('user_id', Integer),
    Column('role', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

organisations = Table(
    'organisations', metadata,
    Column('id', Integer, primary_key=True),
    Column('code', String),
    Column('type', String),
    Column('name', String),
    Column('recruitment', String),
)

organisation_consultants = Table(
    'organisation_consultants', metadata,
    Column('id', Integer, primary_key=True),
    Column('organisation_id', Integer),
    Column('consultant_id', Integer),
)

organisation_patients = Table(
    'organisation_patients', metadata,
    Column('id', Integer, primary_key=True),
    Column('organisation_id', Integer),
    Column('patient_id', Integer),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

organisation_users = Table(
    'organisation_users', metadata,
    Column('id', Integer, primary_key=True),
    Column('organisation_id', Integer),
    Column('user_id', Integer),
    Column('role', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

data_sources = Table(
    'data_sources', metadata,
    Column('id', Integer, primary_key=True),
    Column('organisation_id', Integer, ForeignKey('organisations.id')),
    Column('type', String),
)

consultants = Table(
    'consultants', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String),
    Column('first_name', String),
    Column('last_name', String),
    Column('email', String),
)

patient_aliases = Table(
    'patient_aliases', metadata,
    Column('id', UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('data_source_id', Integer),
    Column('first_name', String),
    Column('last_name', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

patient_addresses = Table(
    'patient_addresses', metadata,
    Column('id', UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('data_source_id', Integer),
    Column('address1', String),
    Column('address2', String),
    Column('address3', Integer),
    Column('postcode', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

patient_consultants = Table(
    'patient_consultants', metadata,
    Column('id', UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('consultant_id', Integer),
    Column('from_date', Date),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

patient_demographics = Table(
    'patient_demographics', metadata,
    Column('id', UUID, primary_key=True),
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

patient_numbers = Table(
    'patient_numbers', metadata,
    Column('id', UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('data_source_id', Integer),
    Column('organisation_id', Integer),
    Column('number', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

hospitalisations = Table(
    'hospitalisations', metadata,
    Column('id', UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('data_source_id', Integer),
    Column('date_of_admission', DateTime),
    Column('date_of_discharge', DateTime),
    Column('reason_for_admission', String),
    Column('comments', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

pathology = Table(
    'pathology', metadata,
    Column('id', UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('data_source_id', Integer),
    Column('date', Date),
    Column('kidney_type', String),
    Column('kidney_side', String),
    Column('reference_number', String),
    Column('histological_summary', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

dialysis = Table(
    'dialysis', metadata,
    Column('id', UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('data_source_id', Integer),
    Column('from_date', Date),
    Column('to_date', Date),
    Column('modality', Integer),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

family_history = Table(
    'family_history', metadata,
    Column('id', UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('cohort_id', Integer),
    Column('parental_consanguinity', Boolean),
    Column('family_history', Boolean),
    Column('other_family_history', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

family_history_relatives = Table(
    'family_history_relatives', metadata,
    Column('id', Integer, primary_key=True),
    Column('family_history_id', Integer),
    Column('relationship', Integer),
    Column('patient_id', Integer),
)

plasmapheresis = Table(
    'plasmapheresis', metadata,
    Column('id', UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('data_source_id', Integer),
    Column('from_date', Date),
    Column('to_date', Date),
    Column('no_of_exchanges', String),
    Column('response', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

medications = Table(
    'medications', metadata,
    Column('id', UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('data_source_id', Integer),
    Column('from_date', Date),
    Column('to_date', Date),
    Column('name', String),
    Column('unstructured', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

genetics = Table(
    'genetics', metadata,
    Column('id', UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('cohort_id', Integer),
    Column('date_sent', Date),
    Column('laboratory', String),
    Column('reference_number', String),
    Column('karyotype', Integer),
    Column('results', String),
    Column('summary', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

alport_clinical_pictures = Table(
    'alport_clinical_pictures', metadata,
    Column('id', UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('date_of_picture', Date),
    Column('deafness', Integer),
    Column('deafness_date', Date),
    Column('hearing_aid_date', Date),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)
