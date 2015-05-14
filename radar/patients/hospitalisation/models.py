from radar.models import DataSource, PatientMixin, CreatedModifiedMixin, UnitMixin
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text


class Hospitalisation(DataSource, PatientMixin, CreatedModifiedMixin, UnitMixin):
    __tablename__ = 'hospitalisations'

    id = Column(Integer, ForeignKey('data_sources.id'), primary_key=True)

    date_of_admission = Column(DateTime(timezone=True))
    date_of_discharge = Column(DateTime(timezone=True))
    reason_for_admission = Column(Text)
    comments = Column(Text)

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user)

    __mapper_args__ = {
        'polymorphic_identity': 'hospitalisations',
    }