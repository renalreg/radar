from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.lib.models.common import MetaModelMixin


class Pathology(db.Model, MetaModelMixin):
    __tablename__ = 'pathology'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')
