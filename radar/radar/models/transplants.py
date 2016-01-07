from collections import OrderedDict

from sqlalchemy import Column, Integer, ForeignKey, Date, Index, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship

TRANSPLANT_MODALITIES = OrderedDict([
    (21, 'Live - Sibling'),
    (74, 'Live - Father'),
    (75, 'Live - Mother'),
    (77, 'Live - Child'),
    (23, 'Live - Other Relative'),
    (24, 'Live - Gentically Unrelated'),
    (26, 'Live - With Transplant Of Other Organ'),
    (27, 'Live - Non-UK'),
    (20, 'Cadaver'),
    (25, 'Cadaver - With Transplant Of Other Organ'),
    (28, 'Non-Heart-Beating'),
    (29, 'Unknown'),
])


class Transplant(db.Model, MetaModelMixin):
    __tablename__ = 'transplants'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('transplants')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    organisation_id = Column(Integer, ForeignKey('organisations.id'), nullable=False)
    organisation = relationship('Organisation')

    date = Column(Date, nullable=False)
    modality = Column(Integer, nullable=False)
    date_of_recurrence = Column(Date)
    date_of_failure = Column(Date)

Index('transplants_patient_id_idx', Transplant.patient_id)


class TransplantRejection(db.Model):
    __tablename__ = 'transplant_rejections'

    id = Column(Integer, primary_key=True)

    transplant_id = Column(UUID, ForeignKey('transplants.id'), nullable=False)
    transplant = relationship('Transplant', backref=backref('rejections', cascade='all, delete-orphan', passive_deletes=True))

    date_of_rejection = Column(Date, nullable=False)

Index('transplant_rejections_transplant_id_idx', TransplantRejection.transplant_id)


class TransplantBiopsy(db.Model):
    __tablename__ = 'transplant_biopsies'

    id = Column(Integer, primary_key=True)

    transplant_id = Column(UUID, ForeignKey('transplants.id'), nullable=False)
    transplant = relationship('Transplant', backref=backref('biopsies', cascade='all, delete-orphan', passive_deletes=True))

    date_of_biopsy = Column(Date, nullable=False)
    recurrence = Column(Boolean, nullable=False)

Index('transplant_biopsies_transplant_id_idx', TransplantBiopsy.transplant_id)
