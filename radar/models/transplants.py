from collections import OrderedDict

from sqlalchemy import Column, Integer, ForeignKey, Date, Index, Boolean, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects import postgresql

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship
from radar.models.logs import log_changes


TRANSPLANT_MODALITIES = OrderedDict([
    (21, 'Live - Sibling'),
    (74, 'Live - Father'),
    (75, 'Live - Mother'),
    (77, 'Live - Child'),
    (23, 'Live - Other Relative'),
    (24, 'Live - Gentically Unrelated'),
    (26, 'Live - With Transplant of Other Organ'),
    (27, 'Live - Non-UK'),
    (20, 'Cadaver'),
    (25, 'Cadaver - With Transplant of Other Organ'),
    (28, 'Non-Heart-Beating'),
    (29, 'Unknown'),
])


@log_changes
class Transplant(db.Model, MetaModelMixin):
    __tablename__ = 'transplants'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('transplants')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group', foreign_keys=[source_group_id])
    source_type = Column(String, nullable=False)

    transplant_group_id = Column(Integer, ForeignKey('groups.id'))
    transplant_group = relationship('Group', foreign_keys=[transplant_group_id])

    date = Column(Date, nullable=False)
    modality = Column(Integer, nullable=False)
    date_of_recurrence = Column(Date)
    date_of_failure = Column(Date)

    @property
    def modality_description(self):
        return TRANSPLANT_MODALITIES.get(self.modality)

Index('transplants_patient_idx', Transplant.patient_id)


@log_changes
class TransplantRejection(db.Model):
    __tablename__ = 'transplant_rejections'

    id = Column(Integer, primary_key=True)

    transplant_id = Column(postgresql.UUID, ForeignKey('transplants.id'), nullable=False)
    transplant = relationship('Transplant', backref=backref('rejections', cascade='all, delete-orphan', passive_deletes=True))

    date_of_rejection = Column(Date, nullable=False)

Index('transplant_rejections_transplant_idx', TransplantRejection.transplant_id)


@log_changes
class TransplantBiopsy(db.Model):
    __tablename__ = 'transplant_biopsies'

    id = Column(Integer, primary_key=True)

    transplant_id = Column(postgresql.UUID, ForeignKey('transplants.id'), nullable=False)
    transplant = relationship('Transplant', backref=backref('biopsies', cascade='all, delete-orphan', passive_deletes=True))

    date_of_biopsy = Column(Date, nullable=False)
    recurrence = Column(Boolean, nullable=False)

Index('transplant_biopsies_transplant_idx', TransplantBiopsy.transplant_id)
