from sqlalchemy import Integer, Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from radar.database import Base


class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

class SDAContainer(Base):
    __tablename__ = 'sda_containers'

    id = Column(Integer, primary_key=True)
    sda_medications = relationship('SDAMedication', backref='sda_container', cascade='all, delete-orphan')

class SDAMedication(Base):
    __tablename__ = 'sda_medications'

    id = Column(Integer, primary_key=True)
    sda_container_id = Column(Integer, ForeignKey('sda_containers.id'))
    from_time = Column(DateTime)
    to_time = Column(DateTime)

