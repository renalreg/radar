from radar.models import DataSource, CreatedModifiedMixin, PatientMixin, DiseaseGroupMixin
from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime


class Genetics(DataSource, CreatedModifiedMixin, PatientMixin, DiseaseGroupMixin):
    __tablename__ = 'genetics'

    id = Column(Integer, ForeignKey('data_sources.id'), primary_key=True)

    sample_sent_date = Column(DateTime(timezone=True))
    laboratory = Column(String)
    laboratory_reference_number = Column(String)
    results = Column(Text)

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user)

    __mapper_args__ = {
        'polymorphic_identity': 'genetics',
    }