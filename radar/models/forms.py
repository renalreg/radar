from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql

from radar.database import db
from radar.models.common import uuid_pk_column, MetaModelMixin, patient_id_column, patient_relationship
from radar.models.logs import log_changes


class Form(db.Model):
    __tablename__ = 'forms'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    data = Column(postgresql.JSONB, nullable=False)


@log_changes
class Entry(db.Model, MetaModelMixin):
    __tablename__ = 'entries'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('entries')

    form_id = Column(Integer, ForeignKey('forms.id'), nullable=False)
    form = relationship('Form')

    data = Column(postgresql.JSONB, nullable=False)


class GroupForm(db.Model):
    __tablename__ = 'group_forms'

    id = Column(Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship('Group')

    form_id = Column(Integer, ForeignKey('forms.id'), nullable=False)
    form = relationship('Form')