from radar.database import db
from radar.models import DataSource, PatientMixin, CreatedModifiedMixin, LookupTableMixin
from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship


class Transplant(DataSource, PatientMixin, CreatedModifiedMixin):
    __tablename__ = 'transplants'

    id = Column(Integer, ForeignKey('data_sources.id'), primary_key=True)

    date = Column(Date)
    transplant_type_id = Column(Integer, ForeignKey('transplant_types.id'), nullable=False)
    transplant_type = relationship('TransplantType')

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user)

    __mapper_args__ = {
        'polymorphic_identity': 'transplants',
    }


class TransplantTypes(db.Model, LookupTableMixin):
    __table_name__ = 'transplant_types'