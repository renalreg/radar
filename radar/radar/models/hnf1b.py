from collections import OrderedDict

from sqlalchemy import Column, Boolean, String, Date, Index

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship

NO_DIABETES = 'NO'

TYPES_OF_DIABETES = OrderedDict([
    (NO_DIABETES, 'No'),
    ('TYPE_1', 'Type I'),
    ('TYPE_2', 'Type II'),
    ('TYPE_2_MODY', 'Type II MODY'),
])


class Hnf1bClinicalPicture(db.Model, MetaModelMixin):
    __tablename__ = 'hnf1b_clinical_pictures'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('hnf1b_clinical_pictures')

    date_of_picture = Column(Date, nullable=False)
    single_kidney = Column(Boolean)
    hyperuricemia_gout = Column(Boolean)
    genital_malformation = Column(Boolean)
    genital_malformation_details = Column(String)
    familial_cystic_disease = Column(Boolean)
    hypertension = Column(Boolean)
    type_of_diabetes = Column(String)
    date_of_diabetes = Column(Date)
    diabetic_nephropathy = Column(Boolean)
    diabetic_retinopathy = Column(Boolean)
    diabetic_neuropathy = Column(Boolean)
    diabetic_pvd = Column(Boolean)

Index('hnf1b_clinical_pictures_patient_idx', Hnf1bClinicalPicture.patient_id)
