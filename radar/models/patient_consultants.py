from sqlalchemy import Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship
from radar.models.logs import log_changes


@log_changes
class PatientConsultant(db.Model, MetaModelMixin):
    __tablename__ = 'patient_consultants'

    id = Column(Integer, primary_key=True)

    patient_id = patient_id_column()
    patient = patient_relationship('patient_consultants')

    consultant_id = Column(Integer, ForeignKey('consultants.id'), nullable=False)
    consultant = relationship('Consultant')

    from_date = Column(Date, nullable=False)
    to_date = Column(Date)
