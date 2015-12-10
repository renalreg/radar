from collections import OrderedDict

from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, Index
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship


RELATIVES = OrderedDict([
    (1, 'Mother'),
    (2, 'Father'),
    (3, 'Sister'),
    (4, 'Brother'),
    (5, 'Grandmother - Maternal'),
    (6, 'Grandmother - Paternal'),
    (15, 'Grandfather - Maternal'),
    (16, 'Grandfather - Paternal'),
    (7, 'Aunt - Maternal'),
    (8, 'Aunt - Paternal'),
    (9, 'Uncle - Maternal'),
    (10, 'Uncle - Paternal'),
    (11, 'Cousin - Maternal'),
    (12, 'Cousin - Paternal'),
    (13, 'Half Sister'),
    (14, 'Half Brother'),
])


class FamilyHistory(db.Model, MetaModelMixin):
    __tablename__ = 'family_history'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('family_history')

    cohort_id = Column(Integer, ForeignKey('cohorts.id'), nullable=False)
    cohort = relationship('Cohort')

    parental_consanguinity = Column(Boolean, nullable=False)
    family_history = Column(Boolean, nullable=False)
    other_family_history = Column(String)

Index('family_history_patient_id_idx', FamilyHistory.patient_id)
Index('family_history_cohort_id_idx', FamilyHistory.cohort_id)


class FamilyHistoryRelative(db.Model):
    __tablename__ = 'family_history_relatives'

    id = Column(Integer, primary_key=True)

    family_history_id = Column(Integer, ForeignKey('family_history.id'), nullable=False)
    family_history = relationship('FamilyHistory')

    relative = Column(Integer, nullable=False)

    # TODO null when patient is deleted
    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship('Patient')

Index('family_history_relatives_family_history_id_idx', FamilyHistoryRelative.family_history_id)
