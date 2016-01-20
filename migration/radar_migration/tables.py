from sqlalchemy import MetaData, Table, Column, Integer, String, Date, DateTime, Boolean
from sqlalchemy.dialects import postgresql

metadata = MetaData()

patients = Table(
    'patients', metadata,
    Column('id', Integer, primary_key=True),
    Column('comments', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String),
    Column('password', String),
    Column('first_name', String),
    Column('last_name', String),
    Column('email', String),
    Column('is_admin', Boolean),
)

groups = Table(
    'groups', metadata,
    Column('id', Integer, primary_key=True),
    Column('type', String),
    Column('code', String),
    Column('name', String),
    Column('short_name', String),
    Column('recruitment', Boolean),
    Column('pages', postgresql.ARRAY(String)),
)

group_diagnoses = Table(
    'group_diagnoses', metadata,
    Column('id', Integer, primary_key=True),
    Column('group_id', Integer),
    Column('name', String),
    Column('display_order', String),
)

group_patients = Table(
    'group_patients', metadata,
    Column('id', Integer, primary_key=True),
    Column('group_id', Integer),
    Column('patient_id', Integer),
    Column('created_group_id', Integer),
    Column('from_date', DateTime),
    Column('to_date', DateTime),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

group_users = Table(
    'group_users', metadata,
    Column('id', Integer, primary_key=True),
    Column('group_id', Integer),
    Column('user_id', Integer),
    Column('role', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

group_consultants = Table(
    'group_consultants', metadata,
    Column('id', Integer, primary_key=True),
    Column('group_id', Integer),
    Column('consultant_id', Integer),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

organisation_patients = Table(
    'organisation_patients', metadata,
    Column('id', Integer, primary_key=True),
    Column('organisation_id', Integer),
    Column('patient_id', Integer),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
    Column('created_date', DateTime),
    Column('modified_date', DateTime),
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

consultants = Table(
    'consultants', metadata,
    Column('id', Integer, primary_key=True),
    Column('first_name', String),
    Column('last_name', String),
    Column('email', String),
    Column('telephone_number', String),
    Column('gmc_number', Integer),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

patient_aliases = Table(
    'patient_aliases', metadata,
    Column('id', postgresql.UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('source_group_id', Integer),
    Column('source_type', String),
    Column('first_name', String),
    Column('last_name', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

patient_addresses = Table(
    'patient_addresses', metadata,
    Column('id', postgresql.UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('source_group_id', Integer),
    Column('source_type', String),
    Column('address_1', String),
    Column('address_2', String),
    Column('address_3', Integer),
    Column('postcode', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

patient_consultants = Table(
    'patient_consultants', metadata,
    Column('id', postgresql.UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('consultant_id', Integer),
    Column('from_date', Date),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

patient_demographics = Table(
    'patient_demographics', metadata,
    Column('id', postgresql.UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('source_group_id', Integer),
    Column('source_type', String),
    Column('first_name', String),
    Column('last_name', String),
    Column('date_of_birth', Date),
    Column('gender', Integer),
    Column('ethnicity', String),
    Column('home_number', String),
    Column('mobile_number', String),
    Column('email_address', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

patient_numbers = Table(
    'patient_numbers', metadata,
    Column('id', postgresql.UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('source_group_id', Integer),
    Column('source_type', String),
    Column('number_group_id', Integer),
    Column('number', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

hospitalisations = Table(
    'hospitalisations', metadata,
    Column('id', postgresql.UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('source_group_id', Integer),
    Column('source_type', String),
    Column('date_of_admission', DateTime),
    Column('date_of_discharge', DateTime),
    Column('reason_for_admission', String),
    Column('comments', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

pathology = Table(
    'pathology', metadata,
    Column('id', postgresql.UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('source_group_id', Integer),
    Column('source_type', String),
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
    Column('id', postgresql.UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('source_group_id', Integer),
    Column('source_type', String),
    Column('from_date', Date),
    Column('to_date', Date),
    Column('modality', Integer),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

family_histories = Table(
    'family_histories', metadata,
    Column('id', postgresql.UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('group_id', Integer),
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
    Column('id', postgresql.UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('source_group_id', Integer),
    Column('source_type', String),
    Column('from_date', Date),
    Column('to_date', Date),
    Column('no_of_exchanges', String),
    Column('response', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

medications = Table(
    'medications', metadata,
    Column('id', postgresql.UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('source_group_id', Integer),
    Column('source_type', String),
    Column('drug_id', Integer),
    Column('from_date', Date),
    Column('to_date', Date),
    Column('dose_quantity', String),
    Column('drug_text', String),
    Column('dose_text', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

genetics = Table(
    'genetics', metadata,
    Column('id', postgresql.UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('group_id', Integer),
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
    Column('id', postgresql.UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('date_of_picture', Date),
    Column('deafness', Integer),
    Column('deafness_date', Date),
    Column('hearing_aid_date', Date),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

ins_relapses = Table(
    'ins_relapses', metadata,
    Column('id', postgresql.UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('date_of_relapse', Date),
    Column('kidney_type', String),
    Column('viral_trigger', String),
    Column('immunisation_trigger', String),
    Column('other_trigger', String),
    Column('high_dose_oral_prednisolone', Boolean),
    Column('iv_methyl_prednisolone', Boolean),
    Column('date_of_remission', Date),
    Column('remission_type', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

transplants = Table(
    'transplants', metadata,
    Column('id', postgresql.UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('source_group_id', Integer),
    Column('source_type', String),
    Column('transplant_group_id', Integer),
    Column('date', Date),
    Column('modality', Integer),
    Column('date_of_recurrence', Date),
    Column('date_of_failure', Date),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

transplant_rejections = Table(
    'transplant_rejections', metadata,
    Column('id', Integer, primary_key=True),
    Column('transplant_id', Integer),
    Column('date_of_rejection', Date),
)

transplant_biopsies = Table(
    'transplant_biopsies', metadata,
    Column('id', Integer, primary_key=True),
    Column('transplant_id', Integer),
    Column('date_of_biopsy', Date),
    Column('recurrence', Boolean),
)

hnf1b_clinical_pictures = Table(
    'hnf1b_clinical_pictures', metadata,
    Column('id', postgresql.UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('date_of_picture', Date),
    Column('single_kidney', Boolean),
    Column('hyperuricemia_gout', Boolean),
    Column('genital_malformation', Boolean),
    Column('genital_malformation_details', String),
    Column('familial_cystic_disease', Boolean),
    Column('hypertension', Boolean),
    Column('type_of_diabetes', String),
    Column('date_of_diabetes', Date),
    Column('diabetic_nephropathy', Boolean),
    Column('diabetic_retinopathy', Boolean),
    Column('diabetic_neuropathy', Boolean),
    Column('diabetic_pvd', Boolean),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

observations = Table(
    'observations', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('short_name', String),
    Column('value_type', String),
    Column('sample_type', String),
    Column('pv_code', String),
    Column('properties', postgresql.JSONB),
)

results = Table(
    'results', metadata,
    Column('id', postgresql.UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('source_group_id', Integer),
    Column('source_type', String),
    Column('observation_id', Integer),
    Column('date', DateTime),
    Column('value', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

diagnoses = Table(
    'diagnoses', metadata,
    Column('id', postgresql.UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('group_id', Integer),
    Column('date_of_diagnosis', Integer),
    Column('group_diagnosis_id', Integer),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

comorbidities = Table(
    'comorbidities', metadata,
    Column('id', postgresql.UUID, primary_key=True),
    Column('patient_id', Integer),
    Column('source_group_id', Integer),
    Column('source_type', String),
    Column('disorder_id', Integer),
    Column('from_date', Date),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

disorders = Table(
    'disorders', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
)

mpgn_clinical_pictures = Table(
    'mpgn_clinical_pictures', metadata,
    Column('patient_id', Integer),
    Column('date_of_picture', Date),
    Column('oedema', Boolean),
    Column('hypertension', Boolean),
    Column('urticaria', Boolean),
    Column('partial_lipodystrophy', Boolean),
    Column('recent_infection', Boolean),
    Column('recent_infection_details', String),
    Column('ophthalmoscopy', Boolean),
    Column('ophthalmoscopy_details', String),
    Column('comments', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

ins_clinical_pictures = Table(
    'ins_clinical_pictures', metadata,
    Column('id', Integer, primary_key=True),
    Column('patient_id', Integer),
    Column('date_of_picture', Integer),
    Column('oedema', Boolean),
    Column('hypovalaemia', Boolean),
    Column('fever', Boolean),
    Column('thrombosis', Boolean),
    Column('peritonitis', Boolean),
    Column('pulmonary_odemea', Boolean),
    Column('hypertension', Boolean),
    Column('rash', Boolean),
    Column('rash_details', String),
    Column('possible_immunisation_trigger', Boolean),
    Column('ophthalmoscopy', Boolean),
    Column('ophthalmoscopy_details', String),
    Column('comments', String),
    Column('created_user_id', Integer),
    Column('modified_user_id', Integer),
)

drugs = Table(
    'drugs', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('parent_drug_id', Integer),
)

drug_types = Table(
    'drug_types', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
)
