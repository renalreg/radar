from collections import OrderedDict

from sqlalchemy import Boolean, Column, Date, Float, Index, String

from radar.database import db
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship, uuid_pk_column
from radar.models.logs import log_changes


KIDNEY_TYPES = OrderedDict([
    ('TRANSPLANT', 'Transplant'),
    ('NATIVE', 'Native'),
])

REMISSION_TYPES = OrderedDict([
    ('COMPLETE', 'Complete'),
    ('PARTIAL', 'Partial'),
    ('NONE', 'None'),
])

DIPSTICK_TYPES = OrderedDict([
    ('NEGATIVE', 'Negative'),
    ('ONEPLUS', '+'),
    ('TWOPLUS', '++'),
    ('THREEPLUS', '+++'),
    ('FOURPLUS', '++++'),
    ('TRACE', 'Trace'),
])


@log_changes
class InsClinicalPicture(db.Model, MetaModelMixin):
    __tablename__ = 'ins_clinical_pictures'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('ins_clinical_pictures')

    date_of_picture = Column(Date, nullable=False)
    oedema = Column(Boolean)
    hypovalaemia = Column(Boolean)
    fever = Column(Boolean)
    thrombosis = Column(Boolean)
    peritonitis = Column(Boolean)
    pulmonary_odemea = Column(Boolean)
    hypertension = Column(Boolean)
    rash = Column(Boolean)
    rash_details = Column(String)
    infection = Column(Boolean)
    infection_details = Column(String)
    ophthalmoscopy = Column(Boolean)
    ophthalmoscopy_details = Column(String)
    comments = Column(String)


Index('ins_clinical_pictures_patient_idx', InsClinicalPicture.patient_id)


@log_changes
class InsRelapse(db.Model, MetaModelMixin):
    __tablename__ = 'ins_relapses'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('ins_relapses')

    date_of_relapse = Column(Date, nullable=False)
    kidney_type = Column(String)
    viral_trigger = Column(String)
    immunisation_trigger = Column(String)
    other_trigger = Column(String)
    peak_pcr = Column(Float)
    peak_acr = Column(Float)
    peak_protein_dipstick = Column(String)
    remission_protein_dipstick = Column(String)
    high_dose_oral_prednisolone = Column(Boolean)
    iv_methyl_prednisolone = Column(Boolean)
    relapse_sample_taken = Column(Boolean)
    date_of_remission = Column(Date)
    remission_type = Column(String)
    remission_pcr = Column(Float)
    remission_acr = Column(Float)

    @property
    def kidney_type_label(self):
        return KIDNEY_TYPES.get(self.kidney_type)

    @property
    def remission_type_label(self):
        return REMISSION_TYPES.get(self.remission_type)


Index('ins_relapses_patient_idx', InsRelapse.patient_id)
