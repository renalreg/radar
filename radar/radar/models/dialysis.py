from sqlalchemy import Column, Integer, ForeignKey, Date, Index
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, IntegerLookupTable, uuid_pk_column, \
    patient_id_column, patient_relationship


class Dialysis(db.Model, MetaModelMixin):
    __tablename__ = 'dialysis'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('dialysis')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    from_date = Column(Date, nullable=False)
    to_date = Column(Date)

    dialysis_type_id = Column(Integer, ForeignKey('dialysis_types.id'), nullable=False)
    dialysis_type = relationship('DialysisType')

Index('dialysis_patient_id_idx', Dialysis.patient_id)


class DialysisType(IntegerLookupTable):
    __tablename__ = 'dialysis_types'
