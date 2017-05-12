#! -*- coding: utf-8 -*-

from collections import OrderedDict

from sqlalchemy import Column, Date, Index, Integer, String

from radar.database import db
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship, uuid_pk_column
from radar.models.logs import log_changes


ADULT = 'ADULT'
CHILDREN_30_PLUS_FIRST = 'CHILDREN30+B'
CHILDREN_30_PLUS_SECOND = 'CHILDREN30+2ND'
CHILDREN_15_PLUS_FIRST = 'CHILDREN15+B'
CHILDREN_15_PLUS_SECOND = 'CHILDREN15+2ND'
CHILDREN_15_LESS_FIRST = 'CHILDREN15-B'
CHILDREN_15_LESS_SECOND = 'CHILDREN15-2ND'

PROTOCOL_OPTIONS = OrderedDict((
    {'id': ADULT, 'label': 'Adult'},
    (CHILDREN_30_PLUS_FIRST, 'Children >30kg NS Baseline, Disease F.Up'),
    (CHILDREN_30_PLUS_SECOND, 'Children >30kg NS 2nd visit'),
    (CHILDREN_15_PLUS_FIRST, 'Children 15-30kg NS Baseline, Disease F.Up'),
    (CHILDREN_15_PLUS_SECOND, 'Children 15-30kg NS 2nd visit'),
    (CHILDREN_15_LESS_FIRST, 'Children <15kg NS Baseline, Disease F.Up'),
    (CHILDREN_15_LESS_SECOND, 'Children <15kg NS 2nd visit'),
))


@log_changes
class Samples(db.Model, MetaModelMixin):
    __tablename__ = 'nurture_samples'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('nurture_samples')

    taken_on = Column(Date, nullable=False)
    barcode  = Column(Integer, nullable=False)
    protocol = Column(String, nullable=False)

    epa = Column(Integer, nullable=True)  # EDTA plasma Tube A 100μl
    epb = Column(Integer, nullable=True)  # EDTA plasma Tube B 1ml

    lpa = Column(Integer)
    lpb = Column(Integer)

    uc = Column(Integer)
    ub = Column(Integer)
    ud = Column(Integer)

    fub = Column(Integer)

    sc = Column(Integer)
    sa = Column(Integer)
    sb = Column(Integer)

    rna = Column(Integer)

    wb = Column(Integer)


Index('samples_patient_idx', Samples.patient_id)
