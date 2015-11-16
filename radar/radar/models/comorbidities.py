from sqlalchemy import Column, Integer, ForeignKey, Date, Index
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models import MetaModelMixin, IntegerLookupTable
from radar.models.common import uuid_pk_column, patient_id_column, patient_relationship


class Comorbidity(db.Model, MetaModelMixin):
    __tablename__ = 'comorbidities'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('comorbidities')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    from_date = Column(Date, nullable=False)
    to_date = Column(Date)

    disorder_id = Column(Integer, ForeignKey('disorders.id'), nullable=False)
    disorder = relationship('Disorder')

Index('comorbidities_patient_id_idx', Comorbidity.patient_id)


class Disorder(IntegerLookupTable):
    __tablename__ = 'disorders'
