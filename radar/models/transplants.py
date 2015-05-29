from sqlalchemy import Column, Integer, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.models.base import DataSource, PatientMixin, MetadataMixin, LookupTableMixin


class Transplant(DataSource, PatientMixin, MetadataMixin):
    __tablename__ = 'transplants'

    id = Column(Integer, ForeignKey('data_sources.id'), primary_key=True)

    transplant_date = Column(Date)
    transplant_type_id = Column(Integer, ForeignKey('transplant_types.id'), nullable=False)
    transplant_type = relationship('TransplantType')
    reoccurred = Column(Boolean)
    date_reoccurred = Column(Date)
    date_failure = Column(Date)

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user)

    __mapper_args__ = {
        'polymorphic_identity': 'transplants',
    }


class TransplantType(db.Model, LookupTableMixin):
    __tablename__ = 'transplant_types'