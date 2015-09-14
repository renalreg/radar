from collections import OrderedDict
from sqlalchemy import Column, Date, String, ForeignKey, Numeric
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.lib.models.common import MetaModelMixin

MEDICATION_ROUTES = OrderedDict([
    ('ORAL', 'Oral'),
    ('RECTAL', 'Rectal'),
])

MEDICATION_DOSE_UNITS = OrderedDict([
    ('ML', 'ml'),
    ('L', 'l'),
    ('MG', 'mg'),
    ('G', 'g'),
    ('KG', 'kg'),
])

MEDICATION_FREQUENCIES = OrderedDict([
    ('DAILY', 'Daily'),
    ('WEEKLY', 'Weekly'),
    ('MONTHLY', 'Monthly'),
])


class Medication(db.Model, MetaModelMixin):
    __tablename__ = 'medications'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    from_date = Column(Date, nullable=False)
    to_date = Column(Date)
    name = Column(String, nullable=False)
    dose_quantity = Column(Numeric, nullable=False)
    dose_unit = Column(String, nullable=False)
    frequency = Column(String, nullable=False)
    route = Column(String, nullable=False)
