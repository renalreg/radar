from sqlalchemy import Column, Integer, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from radar.database import db
from radar.models import MetaModelMixin


class PatientConsultant(db.Model, MetaModelMixin):
    __tablename__ = 'patient_consultants'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    consultant_id = Column(Integer, ForeignKey('consultants.id'), nullable=False)
    consultant = relationship('Consultant')

    __table_args__ = (
        UniqueConstraint('patient_id', 'consultant_id'),
    )
