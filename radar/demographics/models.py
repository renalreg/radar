from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from radar.models import Resource


class Demographics(Resource):
    __tablename__ = 'demographics'

    id = Column(Integer, ForeignKey('resources.id'), primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship('Patient')

    first_name = Column(String)
    last_name = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'demographics',
    }