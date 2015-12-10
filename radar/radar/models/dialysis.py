from collections import OrderedDict

from sqlalchemy import Column, Integer, ForeignKey, Date, Index
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, \
    patient_id_column, patient_relationship


# TODO
TYPES_OF_DIALYSIS = OrderedDict([
    (1, 'Haemodialysis')
])


class Dialysis(db.Model, MetaModelMixin):
    __tablename__ = 'dialysis'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('dialysis')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    from_date = Column(Date, nullable=False)
    to_date = Column(Date)

    type_of_dialysis = Column(Integer, nullable=False)

Index('dialysis_patient_id_idx', Dialysis.patient_id)
