from sqlalchemy import Column, Integer, ForeignKey, Boolean, String

from radar.models.common import DataSource, PatientMixin, MetadataMixin


class SaltWastingClinicalFeatures(DataSource, PatientMixin, MetadataMixin):
    __tablename__ = 'salt_wasting_clinical_features'

    id = Column(Integer, ForeignKey('data_sources.id'), primary_key=True)

    normal_pregnancy = Column(Boolean)
    abnormal_pregnancy_text = Column(String)
    neurological_problems = Column(Boolean)
    seizures = Column(Boolean)
    abnormal_gait = Column(Boolean)
    deafness = Column(Boolean)
    other_neurological_problem = Column(Boolean)
    other_neurological_problem_text = Column(String)
    joint_problems = Column(Boolean)
    join_problems_age = Column(Integer)
    x_ray_abnormalities = Column(Boolean)
    chondrocalcinosis = Column(Boolean)
    other_x_ray_abnormality = Column(Boolean)
    other_x_ray_abnormality_text = Column(String)

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user)

    __mapper_args__ = {
        'polymorphic_identity': 'salt_wasting_clinical_features',
    }