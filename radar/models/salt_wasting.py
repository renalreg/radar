from sqlalchemy import Boolean, Column, Index, Integer, String

from radar.database import db
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship, uuid_pk_column
from radar.models.logs import log_changes


@log_changes
class SaltWastingClinicalFeatures(db.Model, MetaModelMixin):
    __tablename__ = 'salt_wasting_clinical_features'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('salt_wasting_clinical_features')

    normal_pregnancy = Column(Boolean)
    abnormal_pregnancy_text = Column(String)
    neurological_problems = Column(Boolean)
    seizures = Column(Boolean)
    abnormal_gait = Column(Boolean)
    deafness = Column(Boolean)
    other_neurological_problem = Column(Boolean)
    other_neurological_problem_text = Column(String)
    joint_problems = Column(Boolean)
    joint_problems_age = Column(Integer)
    x_ray_abnormalities = Column(Boolean)
    chondrocalcinosis = Column(Boolean)
    other_x_ray_abnormality = Column(Boolean)
    other_x_ray_abnormality_text = Column(String)


Index('salt_wasting_clinical_features_patient_idx', SaltWastingClinicalFeatures.patient_id)
