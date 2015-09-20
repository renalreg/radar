from sqlalchemy import Column, ForeignKey, Date, String, Index
from sqlalchemy import Integer
from sqlalchemy.orm import relationship
from radar.lib.database import db
from radar.lib.models import MetaModelMixin


class PatientAddress(db.Model, MetaModelMixin):
    __tablename__ = 'patient_addresses'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    from_date = Column(Date)
    to_date = Column(Date)
    address_line_1 = Column(String)
    address_line_2 = Column(String)
    address_line_3 = Column(String)
    postcode = Column(String)

    @property
    def full_address(self):
        parts = []

        parts.extend([
            self.address_line_1,
            self.address_line_2,
            self.address_line_3,
            self.postcode,
        ])

        return "\n".join(x for x in parts if x)

Index('patient_addresses_patient_id_idx', PatientAddress.patient_id)
