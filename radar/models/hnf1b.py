from sqlalchemy import Boolean, Column, Date, Index, String

from radar.database import db
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship, uuid_pk_column
from radar.models.logs import log_changes


@log_changes
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


Index('hnf1b_clinical_pictures_patient_idx', Hnf1bClinicalPicture.patient_id)
