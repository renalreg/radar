from collections import OrderedDict

from sqlalchemy import Column, Boolean, String, Index, Date

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship

KIDNEY_TYPES = OrderedDict([
    ('TRANSPLANT', 'Transplant'),
    ('NATIVE', 'Native'),
])

REMISSION_TYPES = OrderedDict([
    ('COMPLETE', 'Complete'),
    ('PARTIAL', 'Partial'),
    ('NONE', 'None'),
])


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
    # TODO complications
    peritonitis = Column(Boolean)
    pulmonary_odemea = Column(Boolean)
    hypertension = Column(Boolean)
    rash = Column(Boolean)
    rash_details = Column(String)
    possible_immunisation_trigger = Column(Boolean)
    ophthalmoscopy = Column(Boolean)
    ophthalmoscopy_details = Column(String)
    comments = Column(String)

Index('ins_clinical_pictures_patient_idx', InsClinicalPicture.patient_id)


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
    high_dose_oral_prednisolone = Column(Boolean)
    iv_methyl_prednisolone = Column(Boolean)
    date_of_remission = Column(Date)
    remission_type = Column(String)

Index('ins_relapses_patient_idx', InsRelapse.patient_id)
