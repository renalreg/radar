from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.lib.models.common import MetaModelMixin, IntegerLookupTable


class Dialysis(db.Model, MetaModelMixin):
    __tablename__ = 'dialysis'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    from_date = Column(Date, nullable=False)
    to_date = Column(Date)

    dialysis_type_id = Column(Integer, ForeignKey('dialysis_types.id'), nullable=False)
    dialysis_type = relationship('DialysisType')


class DialysisType(IntegerLookupTable):
    __tablename__ = 'dialysis_types'
