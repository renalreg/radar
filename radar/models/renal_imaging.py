from sqlalchemy import Column, Integer, ForeignKey, String, Numeric, Boolean, DateTime

from radar.models.base import DataSource, PatientMixin, MetadataMixin


class RenalImaging(DataSource, PatientMixin, MetadataMixin):
    __tablename__ = 'renal_imaging'

    id = Column(Integer, ForeignKey('data_sources.id'), primary_key=True)

    date = Column(DateTime(timezone=True))

    imaging_type = Column(String)

    right_present = Column(Boolean)
    right_type = Column(String)
    right_length = Column(Numeric)
    right_cysts = Column(Numeric)
    right_calcification = Column(String)
    right_nephrocalcinosis = Column(Boolean)
    right_nephrolithiasis = Column(Boolean)
    right_other_malformation = Column(String)

    left_present = Column(Boolean)
    left_type = Column(String)
    left_length = Column(Numeric)
    left_cysts = Column(Numeric)
    left_calcification = Column(String)
    left_nephrocalcinosis = Column(Boolean)
    left_nephrolithiasis = Column(Boolean)
    left_other_malformation = Column(String)

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user)

    __mapper_args__ = {
        'polymorphic_identity': 'renal_imaging',
    }