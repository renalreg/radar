# -*- coding: utf-8 -*-

from collections import OrderedDict

from sqlalchemy import Column, Date, ForeignKey, Index, Numeric, String
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship, uuid_pk_column
from radar.models.logs import log_changes


MEDICATION_ROUTES = OrderedDict([
    ('ORAL', 'Oral'),
    ('IV', 'Intravenous'),
    ('IM', 'Intramuscular'),
    ('SC', 'Subcutaneous'),
    ('PR', 'Per Rectum'),
    ('TOPICAL', 'Topical'),
    ('PATCH', 'Patch'),
    ('INHALE', 'Inhale'),
])

MEDICATION_DOSE_UNITS = OrderedDict([
    ('ML', 'ml'),
    ('UG', u'µg'),
    ('MG', 'mg'),
    ('G', 'g'),
    ('IU', 'IU'),
    ('MMOL', 'mmol'),
    ('PUFF', 'puff'),
    ('UNIT', 'unit'),
])


@log_changes
class CurrentMedication(db.Model, MetaModelMixin):
    __tablename__ = 'current_medications'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('current_medications')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group')
    source_type = Column(String, nullable=False)

    date_recorded = Column(Date, nullable=False)
    drug_id = Column(Integer, ForeignKey('drugs.id'))
    drug = relationship('Drug')
    dose_quantity = Column(Numeric)
    dose_unit = Column(String)
    frequency = Column(String)
    route = Column(String)

    drug_text = Column(String)
    dose_text = Column(String)

    @property
    def dose_unit_label(self):
        return MEDICATION_DOSE_UNITS.get(self.dose_unit)

    @property
    def route_label(self):
        return MEDICATION_ROUTES.get(self.route)


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

    @property
    def dose_unit_label(self):
        return MEDICATION_DOSE_UNITS.get(self.dose_unit)

    @property
    def route_label(self):
        return MEDICATION_ROUTES.get(self.route)


Index('medications_patient_idx', Medication.patient_id)


@log_changes
class Drug(db.Model):
    __tablename__ = 'drugs'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    drug_group_id = Column(Integer, ForeignKey('drug_groups.id'))
    drug_group = relationship('DrugGroup')


@log_changes
class DrugGroup(db.Model):
    __tablename__ = 'drug_groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    parent_drug_group_id = Column(Integer, ForeignKey('drug_groups.id'))
    parent_drug_group = relationship('DrugGroup', remote_side=[id])

    def __unicode__(self):
        return self.name

    __str__ = __unicode__
