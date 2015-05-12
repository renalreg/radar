from radar.models import DataSource, PatientMixin, CreatedModifiedMixin
from sqlalchemy import Column, Integer, ForeignKey


class Dialysis(DataSource, PatientMixin, CreatedModifiedMixin):
    __tablename__ = 'dialysis'

    id = Column(Integer, ForeignKey('data_sources.id'), primary_key=True)

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user)

    __mapper_args__ = {
        'polymorphic_identity': 'dialysis',
    }