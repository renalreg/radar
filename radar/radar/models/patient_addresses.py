from sqlalchemy import Column, ForeignKey, Date, String, Index
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models import MetaModelMixin
from radar.models.common import uuid_pk_column, patient_id_column, patient_relationship


class PatientAddress(db.Model, MetaModelMixin):
    __tablename__ = 'patient_addresses'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('patient_addresses')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group')
    source_id = Column(String, ForeignKey('sources.id'), nullable=False)
    source = relationship('Source')

    from_date = Column(Date)
    to_date = Column(Date)
    address1 = Column(String)
    address2 = Column(String)
    address3 = Column(String)
    postcode = Column(String)

    @property
    def full_address(self):
        parts = []

        parts.extend([
            self.address1,
            self.address2,
            self.address3,
            self.postcode,
        ])

        return "\n".join(x for x in parts if x)

Index('patient_addresses_patient_id_idx', PatientAddress.patient_id)
