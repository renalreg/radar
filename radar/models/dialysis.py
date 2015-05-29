from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.models.base import DataSource, PatientMixin, MetadataMixin, UnitMixin, LookupTableMixin
from radar.lib.concept_maps.dialysis import DialysisConceptMap


class Dialysis(DataSource, PatientMixin, MetadataMixin, UnitMixin):
    __tablename__ = 'dialysis'

    id = Column(Integer, ForeignKey('data_sources.id'), primary_key=True)

    from_date = Column(Date, nullable=False)
    to_date = Column(Date)
    dialysis_type_id = Column(Integer, ForeignKey('dialysis_types.id'), nullable=False)
    dialysis_type = relationship('DialysisType')

    __mapper_args__ = {
        'polymorphic_identity': 'dialysis',
    }

    def concept_map(self):
        return DialysisConceptMap(self)

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user)


class DialysisType(db.Model, LookupTableMixin):
    __tablename__ = 'dialysis_types'