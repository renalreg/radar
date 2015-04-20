from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from radar.database import Base


class Demographics(Base):
    __tablename__ = 'demographics'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship('Patient')

    first_name = Column(String)
    last_name = Column(String)

    sda_container_id = Column(Integer, ForeignKey('sda_containers.id'))
    sda_container = relationship('SDAContainer', cascade='all, delete-orphan', single_parent=True)