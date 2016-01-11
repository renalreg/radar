from sqlalchemy import Column, Integer, ForeignKey, Date, Index, String
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models import MetaModelMixin
from radar.models.common import uuid_pk_column, patient_id_column, patient_relationship


class Comorbidity(db.Model, MetaModelMixin):
    __tablename__ = 'comorbidities'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('comorbidities')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group')
    source_type_id = Column(String, ForeignKey('source_types.id'), nullable=False)
    source_type = relationship('SourceType')

    from_date = Column(Date, nullable=False)
    to_date = Column(Date)

    disorder_id = Column(Integer, ForeignKey('disorders.id'), nullable=False)
    disorder = relationship('Disorder')

Index('comorbidities_patient_id_idx', Comorbidity.patient_id)


class Disorder(db.Model):
    __tablename__ = 'disorders'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
