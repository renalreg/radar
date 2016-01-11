from collections import OrderedDict

from sqlalchemy import Column, Integer, ForeignKey, Date, String, Index
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship
from radar.utils import to_age

DIAGNOSIS_BIOPSY_DIAGNOSES = OrderedDict([
    (1, 'Minimal Change'),
    (2, 'FSGS'),
    (3, 'Mesangial Hyperthrophy'),
    (4, 'Other'),
    (5, 'No BX @ Time of Diagnosis'),
])


class Diagnosis(db.Model, MetaModelMixin):
    __tablename__ = 'diagnoses'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('diagnoses')

    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship('Group')

    date_of_symptoms = Column(Date, nullable=False)
    date_of_diagnosis = Column(Date, nullable=False)
    date_of_renal_disease = Column(Date)

    group_diagnosis_id = Column(Integer, ForeignKey('group_diagnoses.id'), nullable=False)
    group_diagnosis = relationship('GroupDiagnosis')

    diagnosis_text = Column(String)
    biopsy_diagnosis = Column(Integer)

    @property
    def age_of_symptoms(self):
        x = to_age(self.patient, self.date_of_symptoms)
        return x

    @property
    def age_of_diagnosis(self):
        return to_age(self.patient, self.date_of_diagnosis)

    @property
    def age_of_renal_disease(self):
        if self.date_of_renal_disease is None:
            r = None
        else:
            r = to_age(self.patient, self.date_of_renal_disease)

        return r

Index('diagnoses_patient_idx', Diagnosis.patient_id)
Index('diagnoses_group_idx', Diagnosis.group_id)
Index(
    'diagnoses_patient_group_idx',
    Diagnosis.patient_id,
    Diagnosis.group_id,
    unique=True
)


class GroupDiagnosis(db.Model):
    __tablename__ = 'group_diagnoses'

    id = Column(Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship('Group')

    name = Column(String, nullable=False)
    display_order = Column(Integer, nullable=False)

Index('group_diagnoses_group_idx', GroupDiagnosis.group_id)
