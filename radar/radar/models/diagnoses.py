from collections import OrderedDict

from sqlalchemy import Column, Integer, ForeignKey, Date, String, Index, Boolean
from sqlalchemy.orm import relationship
from enum import Enum

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship
from radar.models.types import EnumType
from radar.utils import to_age

BIOPSY_DIAGNOSES = OrderedDict([
    (1, 'Minimal Change'),
    (2, 'FSGS'),
    (3, 'Mesangial Hyperthrophy'),
    (4, 'Other'),
])


class PatientDiagnosis(db.Model, MetaModelMixin):
    __tablename__ = 'patient_diagnoses'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('patient_diagnoses')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group')
    source_type = Column(String, nullable=False)

    diagnosis_id = Column(Integer, ForeignKey('diagnoses.id'))
    diagnosis = relationship('Diagnosis')
    diagnosis_text = Column(String)

    symptoms_date = Column(Date)
    from_date = Column(Date, nullable=False)
    to_date = Column(Date)

    gene_test = Column(Boolean)
    biochemistry = Column(Boolean)
    clinical_picture = Column(Boolean)
    biopsy = Column(Boolean)
    biopsy_diagnosis = Column(Integer)

    comments = Column(String)

    @property
    def symptoms_age(self):
        if self.symptoms_date is None:
            r = None
        else:
            r = to_age(self.patient, self.symptoms_date)

        return r

    @property
    def from_age(self):
        return to_age(self.patient, self.from_date)

    @property
    def to_age(self):
        if self.to_date is None:
            r = None
        else:
            r = to_age(self.patient, self.to_date)

        return r

Index('patient_diagnoses_patient_idx', PatientDiagnosis.patient_id)


class Diagnosis(db.Model):
    __tablename__ = 'diagnoses'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    group_diagnoses = relationship('GroupDiagnosis')

    @property
    def groups(self):
        return [x.group for x in self.group_diagnoses]


class GROUP_DIAGNOSIS_TYPE(Enum):
    PRIMARY = 'PRIMARY'
    SECONDARY = 'SECONDARY'


class GroupDiagnosis(db.Model):
    __tablename__ = 'group_diagnoses'

    id = Column(Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship('Group')

    diagnosis_id = Column(Integer, ForeignKey('diagnoses.id'), nullable=False)
    diagnosis = relationship('Diagnosis')

    type = Column(EnumType(GROUP_DIAGNOSIS_TYPE, name='group_diagnosis_type'), nullable=False)

Index('group_diagnoses_group_idx', GroupDiagnosis.group_id)
Index('group_diagnoses_diagnosis_idx', GroupDiagnosis.group_id)
Index('group_diagnoses_diagnosis_group_idx', GroupDiagnosis.diagnosis_id, GroupDiagnosis.group_id, unique=True)
