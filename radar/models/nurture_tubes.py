#! -*- coding: utf-8 -*-

from enum import Enum

from sqlalchemy import Column, Date, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship, uuid_pk_column
from radar.models.logs import log_changes
from radar.models.types import EnumType


class PROTOCOL_OPTION_TYPE(Enum):
    ADULT_CKD = 'ADULT_CKD'
    ADULT_NS = 'ADULT_NS'
    CHILDREN30_B = 'CHILDREN30_B'
    CHILDREN30_2ND = 'CHILDREN30_2ND'
    CHILDREN15_B = 'CHILDREN15_B'
    CHILDREN15_2ND = 'CHILDREN15_2ND'
    CHILDREN_LESS_15_B = 'CHILDREN_LESS_15_B'
    CHILDREN_LESS_15_2ND = 'CHILDREN_LESS_15_2ND'


class SampleOption(db.Model):
    __tablename__ = 'nurture_samples_options'

    id = Column(EnumType(PROTOCOL_OPTION_TYPE, name='protocol_type'), unique=True, nullable=False, primary_key=True)
    label = Column(String, nullable=False)

    epa = Column(Integer, nullable=True)  # EDTA plasma Tube A 100μl
    epb = Column(Integer, nullable=True)  # EDTA plasma Tube B 1ml

    lpa = Column(Integer)  # Li-Hep plasma (LP) Tube A 100μl
    lpb = Column(Integer)  # Li-Hep plasma (LP) Tube B 1ml

    uc = Column(Integer)  # Urine Complete (U) Tube C
    ub = Column(Integer)  # Urine Complete (U) Tube B
    ud = Column(Integer)  # Urine Complete (U) Tube D, 20ml

    fub = Column(Integer)  # Cell-Free Urine (FU) Tube B

    sc = Column(Integer)  # Serum Tube C
    sa = Column(Integer)  # Serum Tube A
    sb = Column(Integer)  # Serum Tube B

    rna = Column(Integer)  # RNA, PAXgene tube

    wb = Column(Integer)  # Whole blood EDTA (WB)


@log_changes
class Samples(db.Model, MetaModelMixin):
    __tablename__ = 'nurture_samples'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('nurture_samples')

    taken_on = Column(Date, nullable=False)
    barcode = Column(Integer, nullable=False)
    protocol_id = Column(
        EnumType(PROTOCOL_OPTION_TYPE, name='protocol_type'),
        ForeignKey('nurture_samples_options.id'),
        nullable=False
    )
    protocol = relationship('SampleOption')

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
