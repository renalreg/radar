from collections import OrderedDict

from sqlalchemy import Column, Integer, Date, Index, Boolean

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship

OUTCOMES = OrderedDict([
    ('ID_LT_20', 'Intrauterine Death < 20 Weeks'),
    ('ID_GTE_20', 'Intrauterine Death >= 20 Weeks'),
    ('ND', 'Neonatal Death < 28 days'),
    ('LIVE', 'Live Infant'),
])

DELIVERY_METHODS = OrderedDict([
    ('SPONTANEOUS_VAGINAL', 'Spontaneous - Vaginal'),
    ('SPONTANEOUS_CS', 'Spontaneous - Emergency CS'),
    ('INDUCED_VAGINAL', 'Induced - Vaginal'),
    ('INDUCED_CS', 'Induced - Emergency CS'),
    ('ELECTIVE_CS', 'Elective - CS'),
])

PRE_ECLAMPSIA_TYPES = OrderedDict([
    ('NO', 'No'),
    ('IMMINENT', 'Imminent - Delivered Before Overt'),
    ('SUSPECTED', 'Suspected - Insufficient Laboratory Data'),
    ('YES', 'Yes - Clinical and Laboratory Diagnosis'),
])


class Pregnancy(db.Model, MetaModelMixin):
    __tablename__ = 'pregnancies'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('pregnancies')

    pregnancy_number = Column(Integer, nullable=False)
    date_of_lmp = Column(Date, nullable=False)
    gravidity = Column(Integer)
    parity1 = Column(Integer)
    parity2 = Column(Integer)
    outcome = Column(Integer)
    weight = Column(Integer)
    weight_centile = Column(Integer)
    gestational_age = Column(Integer)
    delivery_method = Column(Integer)
    neonatal_intensive_care = Column(Boolean)
    pre_eclampsia = Column(Integer)

Index('pregnancies_patient_idx', Pregnancy.patient_id)
