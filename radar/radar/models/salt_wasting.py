from sqlalchemy import Column, Integer, Boolean, String, Index

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship


class SaltWastingClinicalFeatures(db.Model, MetaModelMixin):
    __tablename__ = 'salt_wasting_clinical_features'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('salt_wasting_clinical_features')

    normal_pregnancy = Column(Boolean, nullable=False)
    abnormal_pregnancy_text = Column(String)
    neurological_problems = Column(Boolean, nullable=False)
    seizures = Column(Boolean)
    abnormal_gait = Column(Boolean)
    deafness = Column(Boolean)
    other_neurological_problem = Column(Boolean)
    other_neurological_problem_text = Column(String)
    joint_problems = Column(Boolean, nullable=False)
    joint_problems_age = Column(Integer)
    x_ray_abnormalities = Column(Boolean)
    chondrocalcinosis = Column(Boolean)
    other_x_ray_abnormality = Column(Boolean)
    other_x_ray_abnormality_text = Column(String)

Index('salt_wasting_clinical_features_patient_id_idx', SaltWastingClinicalFeatures.patient_id)
