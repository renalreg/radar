from collections import OrderedDict

from sqlalchemy import Column, Boolean, String, Date, Integer

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship

NO_DIABETES = 1

TYPES_OF_DIABETES = OrderedDict([
    (NO_DIABETES, 'No'),
    (2, 'Type I'),
    (3, 'Type II'),
    (4, 'Type II MODY'),
])


class Hnf1bClinicalPicture(db.Model, MetaModelMixin):
    __tablename__ = 'hnf1b_clinical_pictures'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('hnf1b_clinical_pictures')

    date_of_picture = Column(Date, nullable=False)
    date_of_renal_disease = Column(Date)
    cysts = Column(Boolean)
    stones = Column(Boolean)
    single_kidney = Column(Boolean)
    other_malformation = Column(Boolean)
    other_malformation_details = Column(String)
    hyperuricemia_gout = Column(Boolean)
    genital_malformation = Column(Boolean)
    genital_malformation_details = Column(String)
    familial_cystic_disease = Column(Boolean)
    hypertension = Column(Boolean)
    type_of_diabetes = Column(Integer)
    date_of_diabetes = Column(Date)
    diabetic_nephropathy = Column(Boolean)
    diabetic_retinopathy = Column(Boolean)
    diabetic_neuropathy = Column(Boolean)
    diabetic_pvd = Column(Boolean)
