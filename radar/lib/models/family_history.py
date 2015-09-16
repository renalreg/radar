from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.lib.models.common import MetaModelMixin


class FamilyHistory(db.Model, MetaModelMixin):
    __tablename__ = 'family_history'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    parental_consanguinity = Column(Boolean, nullable=False)
    family_history = Column(Boolean, nullable=False)
