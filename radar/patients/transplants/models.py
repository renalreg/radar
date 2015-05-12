from radar.models import DataSource, PatientMixin, CreatedModifiedMixin
from sqlalchemy import Column, Integer, ForeignKey


class Transplant(DataSource, PatientMixin, CreatedModifiedMixin):
    __tablename__ = 'transplants'

    id = Column(Integer, ForeignKey('data_sources.id'), primary_key=True)

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user)

    __mapper_args__ = {
        'polymorphic_identity': 'transplants',
    }