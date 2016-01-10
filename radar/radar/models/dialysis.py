from collections import OrderedDict

from sqlalchemy import Column, Integer, ForeignKey, Date, Index, String
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, \
    patient_id_column, patient_relationship

DIALYSIS_MODALITIES = OrderedDict([
    (1, 'Haemodialysis'),
    (2, 'Haemofiltration'),
    (3, 'Haemodiafiltration'),
    (5, 'Ultrafiltration'),
    (11, 'CAPD'),
    (111, 'Assisted CAPD'),
    (12, 'APD'),
    (121, 'Assisted APD'),
    (19, 'Peritoneal Dialysis - Type Unknown'),
    (201, 'Hybrid CAPD with HD'),
    (202, 'Hybrid APD with HD'),
    (203, 'Hybrid APD with CAPD'),
])


class Dialysis(db.Model, MetaModelMixin):
    __tablename__ = 'dialysis'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('dialysis')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group')
    source_id = Column(String, ForeignKey('sources.id'), nullable=False)
    source = relationship('Source')

    from_date = Column(Date, nullable=False)
    to_date = Column(Date)

    modality = Column(Integer, nullable=False)

Index('dialysis_patient_id_idx', Dialysis.patient_id)
