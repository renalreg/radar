from collections import OrderedDict

from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import (
    MetaModelMixin,
    patient_id_column,
    patient_relationship,
    uuid_pk_column,
)
from radar.models.logs import log_changes


PERFORMANCE_STATUS_OPTIONS = OrderedDict(
    [
        (0, "0: able to carry out all normal activity without restriction"),
        (1, "1: restricted in strenuous activity but ambulatory and able to carry out light work"),
        (
            2,
            "2: ambulatory and capable of all self-care but unable to carry out any work activities; up and about more than 50% of waking hours",
        ),  # noqa
        (
            3,
            "3: symptomatic and in a chair or in bed for greater than 50% of the day but not bedridden",
        ),
        (
            4,
            "4: completely disabled; cannot carry out any self-care; totally confined to bed or chair",
        ),
    ]
)


TREATMENT_OPTIONS = OrderedDict(
    [
        ("chlorambucil", "Chlorambucil"),
        ("cyclophosphamide", "Cyclophosphamide"),
        ("rituximab", "Rituximab"),
        ("tacrolimus", "Tacrolimus"),
        ("cyclosporine", "Cyclosporine"),
    ]
)


SUPPORTIVE_MEDICATIONS = OrderedDict(
    [
        ("RAAS_BLOCKADE", "RAAS Blockade"),
        ("ANTICOAGULANT", "Anticoagulant"),
        ("ANTIPLATELET", "Antiplatelet"),
        ("STATINS", "Statins"),
        ("DIURETICS", "Diuretics"),
    ]
)


NEPHROPATHY_TYPES = OrderedDict(
    [
        ("NATIVE_MEMBRANOUS_NEPHROPATHY", "Native membranous nephropathy"),
        ("TRANSPLANT_MEMBRANOUS_NEPHROPATHY", "Transplant membranous nephropathy"),
    ]
)


@log_changes
class BaselineAssessment(db.Model, MetaModelMixin):
    __tablename__ = "rituximab_baseline_assessment"

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship("rituximab_baseline_assessment")

    source_group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    source_group = relationship("Group")
    source_type = Column(String, nullable=False)

    date = Column(Date, nullable=False)
    nephropathy = Column(String)
    comorbidities = Column(Boolean)

    supportive_medication = Column(postgresql.ARRAY(String))
    previous_treatment = Column(postgresql.JSONB)  # [{'name': '', 'start': '', 'end': ''}, ]
    steroids = Column(Boolean)
    other_previous_treatment = Column(String)
    past_remission = Column(Boolean)
    performance_status = Column(Integer)


@log_changes
class RituximabCriteria(db.Model, MetaModelMixin):
    __tablename__ = "rituximab_criteria"

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship("rituximab_criteria")

    date = Column(Date, nullable=False)
    criteria1 = Column(Boolean)
    criteria2 = Column(Boolean)
    criteria3 = Column(Boolean)
    criteria4 = Column(Boolean)
    criteria5 = Column(Boolean)
    criteria6 = Column(Boolean)
    criteria7 = Column(Boolean)

    ongoing_severe_disease = Column(Boolean)
    hypersensitivity = Column(Boolean)
    drug_associated_toxicity = Column(Boolean)
    alkylating_complication = Column(Boolean)
    alkylating_failure_monitoring_requirements = Column(Boolean)
    cancer = Column(Boolean)
    threatened_fertility = Column(Boolean)
    fall_in_egfr = Column(Boolean)
    cni_therapy_complication = Column(Boolean)
    cni_failure_monitoring_requirements = Column(Boolean)
    diabetes = Column(Boolean)
    risk_factors = Column(Boolean)
    previous_hospitalization = Column(Boolean)
    osteoporosis_osteopenia = Column(Boolean)
    mood_disturbance = Column(Boolean)
