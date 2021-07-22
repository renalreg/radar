from collections import OrderedDict
from enum import Enum

from sqlalchemy import Boolean, CheckConstraint, Column, Date, ForeignKey, Index, Integer, String, text
from sqlalchemy.orm import backref, relationship

from radar.database import db
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship, uuid_pk_column
from radar.models.logs import log_changes
from radar.models.types import EnumType


BIOPSY_DIAGNOSES = OrderedDict([
    (1, 'Minimal Change'),
    (2, 'FSGS'),
    (3, 'Mesangial Hyperthrophy'),
    (4, 'Other'),
])


@log_changes
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
    status = Column(Boolean, nullable=False, default=True, server_default=text('true'))
    primary = Column(Boolean, nullable=True)
    swan = Column(Boolean, default=False, server_default=text('false'))

    symptoms_date = Column(Date)
    from_date = Column(Date, nullable=False)
    to_date = Column(Date)

    prenatal = Column(Boolean)
    gene_test = Column(Boolean)
    biochemistry = Column(Boolean)
    clinical_picture = Column(Boolean)
    biopsy = Column(Boolean)
    biopsy_diagnosis = Column(Integer)

    comments = Column(String)

    @property
    def symptoms_age(self):
        """Patient's age (in months) when the symptoms started."""

        if self.symptoms_date is None:
            r = None
        else:
            r = self.patient.to_age(self.symptoms_date)

        return r

    @property
    def from_age(self):
        """Patient's age (in months) when they were diagnosed."""

        return self.patient.to_age(self.from_date)

    @property
    def to_age(self):
        """Patient's age (in months) when they recovered."""

        if self.to_date is None:
            r = None
        else:
            r = self.patient.to_age(self.to_date)

        return r

    @property
    def biopsy_diagnosis_label(self):
        return BIOPSY_DIAGNOSES.get(self.biopsy_diagnosis)

    @property
    def name(self):
        if self.diagnosis:
            return self.diagnosis.name
        else:
            return self.diagnosis_text


Index('patient_diagnoses_patient_idx', PatientDiagnosis.patient_id)


@log_changes
class Diagnosis(db.Model):
    __tablename__ = 'diagnoses'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    retired = Column(Boolean, nullable=False, default=False, server_default=text('false'))

    @property
    def groups(self):
        return [x.group for x in self.group_diagnoses]

    @property
    def codes(self):
        return [x.code for x in self.diagnosis_codes]

    def __str__(self):
        return self.name


class GROUP_DIAGNOSIS_TYPE(Enum):
    PRIMARY = 'PRIMARY'
    SECONDARY = 'SECONDARY'

    def __str__(self):
        return self.value


GROUP_DIAGNOSIS_TYPE_NAMES = OrderedDict([
    (GROUP_DIAGNOSIS_TYPE.PRIMARY, 'Primary'),
    (GROUP_DIAGNOSIS_TYPE.SECONDARY, 'Secondary'),
])


@log_changes
class GroupDiagnosis(db.Model):
    __tablename__ = 'group_diagnoses'

    id = Column(Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship(
        'Group',
        backref=backref('group_diagnoses')
    )

    diagnosis_id = Column(Integer, ForeignKey('diagnoses.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    diagnosis = relationship(
        'Diagnosis',
        backref=backref('group_diagnoses', cascade='all, delete-orphan', passive_deletes=True))

    type = Column(EnumType(GROUP_DIAGNOSIS_TYPE, name='group_diagnosis_type'), nullable=False)

    weight = Column(Integer, CheckConstraint('weight >= 0'), nullable=False, default=9999, server_default=text('9999'))

    def __str__(self):
        return "{} - {}".format(str(self.group), str(self.weight))


Index('group_diagnoses_group_idx', GroupDiagnosis.group_id)
Index('group_diagnoses_diagnosis_idx', GroupDiagnosis.diagnosis_id)
Index('group_diagnoses_diagnosis_group_idx', GroupDiagnosis.diagnosis_id, GroupDiagnosis.group_id, unique=True)


@log_changes
class DiagnosisCode(db.Model):
    __tablename__ = 'diagnosis_codes'

    id = Column(Integer, primary_key=True)

    diagnosis_id = Column(Integer, ForeignKey('diagnoses.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    diagnosis = relationship(
        'Diagnosis',
        backref=backref('diagnosis_codes', cascade='all, delete-orphan', passive_deletes=True))

    code_id = Column(Integer, ForeignKey('codes.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    code = relationship('Code', backref=backref('diagnosis_codes', cascade='all, delete-orphan', passive_deletes=True))

    def __str__(self):
        return unicode(self.code)


Index('diagnosis_codes_diagnosis_code_idx', DiagnosisCode.diagnosis_id, DiagnosisCode.code_id, unique=True)
