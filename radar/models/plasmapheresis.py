from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import Date
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.models.common import UnitMixin, PatientMixin, MetadataMixin, DataSource, LookupTableMixin


class Plasmapheresis(DataSource, PatientMixin, MetadataMixin, UnitMixin):
    __tablename__ = 'plasmapheresis'

    id = Column(Integer, ForeignKey('data_sources.id'), primary_key=True)

    from_date = Column(Date, nullable=False)
    to_date = Column(Date)
    no_of_exchanges = Column(Integer)
    response_id = Column(Integer, ForeignKey('plasmapheresis_responses.id'))
    response = relationship('PlasmapheresisResponse')

    __mapper_args__ = {
        'polymorphic_identity': 'plasmapheresis',
    }

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user)


class PlasmapheresisResponse(db.Model, LookupTableMixin):
    __tablename__ = 'plasmapheresis_responses'