from sqlalchemy import Column, ForeignKey, Date, String, Index
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship
from radar.models.logs import log_changes


@log_changes
class PatientAddress(db.Model, MetaModelMixin):
    __tablename__ = 'patient_addresses'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('patient_addresses')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group')
    source_type = Column(String, nullable=False)

    from_date = Column(Date)
    to_date = Column(Date)
    address_1 = Column(String)
    address_2 = Column(String)
    address_3 = Column(String)
    address_4 = Column(String)
    postcode = Column(String)

    @property
    def full_address(self):
        parts = []

        parts.extend([
            self.address_1,
            self.address_2,
            self.address_3,
            self.address_4,
            self.postcode,
        ])

        return '\n'.join(x for x in parts if x)

    @property
    def anonymised_postcode(self):
        postcode = self.postcode

        if postcode is None:
            anonymised_postcode = None
        else:
            anonymised_postcode = postcode.split(' ')[0][:4]

        return anonymised_postcode

Index('patient_addresses_patient_idx', PatientAddress.patient_id)
