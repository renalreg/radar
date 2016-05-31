from collections import OrderedDict

from sqlalchemy import Column, Integer, ForeignKey, String, Numeric, Boolean, DateTime, Index, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship
from radar.models.logs import log_changes


LIVER_IMAGING_TYPES = OrderedDict([
    ('USS', 'USS'),
    ('CT', 'CT'),
    ('MRI', 'MRI'),
])


@log_changes
class LiverImaging(db.Model, MetaModelMixin):
    __tablename__ = 'liver_imaging'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('liver_imaging')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group')
    source_type = Column(String, nullable=False)

    date = Column(DateTime(timezone=True), nullable=False)
    imaging_type = Column(String, nullable=False)

    size = Column(Numeric)

    hepatic_fibrosis = Column(Boolean)
    hepatic_cysts = Column(Boolean)
    bile_duct_cysts = Column(Boolean)
    dilated_bile_ducts = Column(Boolean)
    cholangitis = Column(Boolean)

Index('liver_imaging_patient_idx', LiverImaging.patient_id)


@log_changes
class LiverSymptoms(db.Model, MetaModelMixin):
    __tablename__ = 'liver_symptoms'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('liver_symptoms')

    portal_hypertension = Column(Boolean)
    portal_hypertension_date = Column(Date)
    oesophageal = Column(Boolean)
    oesophageal_date = Column(Date)
    oesophageal_bleeding = Column(Boolean)
    oesophageal_bleeding_date = Column(Date)
    gastric = Column(Boolean)
    gastric_date = Column(Date)
    gastric_bleeding = Column(Boolean)
    gastric_bleeding_date = Column(Date)
    anorectal = Column(Boolean)
    anorectal_date = Column(Date)
    anorectal_bleeding = Column(Boolean)
    anorectal_bleeding_date = Column(Date)
    cholangitis_acute = Column(Boolean)
    cholangitis_acute_date = Column(Date)
    cholangitis_recurrent = Column(Boolean)
    cholangitis_recurrent_date = Column(Date)
    spleen_palpable = Column(Boolean)
    spleen_palpable_date = Column(Date)

Index('liver_symptoms_patient_idx', LiverSymptoms.patient_id, unique=True)


INDICATIONS = OrderedDict([
    ('RECURRENT_CHOLANGITIS', 'Recurrent Cholangitis'),
    ('INTRACTIBLE_VARICEAL_BLEEDING', 'Intractible Variceal Bleeding'),
    ('INTRACTIBLE_ASCITES', 'Intractible Ascites'),
])

FIRST_GRAFT_SOURCES = OrderedDict([
    ('LRD', 'LRD - Living Related Donor'),
    ('LUD', 'LUD - Living Unrelated Donor'),
    ('DBD', 'DBD - Donation after Brain Death'),
    ('DCD', 'DCD - Donation after Circulatory Death'),
])

LOSS_REASONS = OrderedDict([
    ('ACUTE_REJECTION', 'Acute Rejection'),
    ('CHRONIC_REJECTION', 'Chronic Rejection'),
    ('INFECTION', 'Infection'),
    ('CHOLANGITIS', 'Cholangitis'),
])


@log_changes
class LiverTransplant(db.Model, MetaModelMixin):
    __tablename__ = 'liver_transplants'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('liver_transplants')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group')
    source_type = Column(String, nullable=False)

    registration_date = Column(Date)
    transplant_date = Column(Date, nullable=False)
    indications = Column(postgresql.ARRAY(String))
    other_indications = Column(String)
    first_graft_source = Column(String)
    loss_reason = Column(String)
    other_loss_reason = Column(String)

Index('liver_transplants_patient_idx', LiverTransplant.patient_id)
