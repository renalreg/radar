# -*- coding: utf-8 -*-

from collections import OrderedDict
from sqlalchemy import Column, Date, String, ForeignKey, Numeric, Index
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship
from radar.models.logs import log_changes


MEDICATION_ROUTES = OrderedDict([
    ('ORAL', 'Oral'),
    ('IV', 'Intravenous'),
    ('IM', 'Intramuscular'),
    ('SC', 'Subcutaneous'),
    ('PR', 'Per Rectum'),
    ('TOPICAL', 'Topical'),
    ('PATCH', 'Patch'),
])

MEDICATION_DOSE_UNITS = OrderedDict([
    ('ML', 'ml'),
    ('UG', u'µg'),
    ('MG', 'mg'),
    ('G', 'g'),
    ('IU', 'IU'),
])


@log_changes
class Medication(db.Model, MetaModelMixin):
    __tablename__ = 'medications'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('medications')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group')
    source_type = Column(String, nullable=False)

    from_date = Column(Date, nullable=False)
    to_date = Column(Date)
    drug_id = Column(Integer, ForeignKey('drugs.id'))
    drug = relationship('Drug')
    dose_quantity = Column(Numeric)
    dose_unit = Column(String)
    frequency = Column(String)
    route = Column(String)

    drug_text = Column(String)
    dose_text = Column(String)

Index('medications_patient_idx', Medication.patient_id)


@log_changes
class Drug(db.Model):
    __tablename__ = 'drugs'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    parent_drug_id = Column(Integer, ForeignKey('drugs.id'))
    parent_drug = relationship('Drug', remote_side=[id])