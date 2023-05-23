from collections import OrderedDict
from datetime import date
from enum import Enum
from itertools import chain
import math
import numpy as np

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    event,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
)
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
from radar.models.patient_codes import GENDER_FEMALE, GENDER_MALE
from radar.models.types import EnumType
from radar.models.z_score_constants import z_score_constants
from radar.utils import pairwise


class OBSERVATION_VALUE_TYPE(Enum):
    INTEGER = "INTEGER"
    REAL = "REAL"
    ENUM = "ENUM"
    STRING = "STRING"

    def __str__(self):
        return str(self.value)


OBSERVATION_VALUE_TYPE_NAMES = OrderedDict(
    [
        (OBSERVATION_VALUE_TYPE.INTEGER, "Integer"),
        (OBSERVATION_VALUE_TYPE.REAL, "Real"),
        (OBSERVATION_VALUE_TYPE.ENUM, "Enum"),
        (OBSERVATION_VALUE_TYPE.STRING, "String"),
    ]
)


class OBSERVATION_SAMPLE_TYPE(Enum):
    URINE = "URINE"
    BLOOD = "BLOOD"
    URINE_DIPSTICK = "URINE_DIPSTICK"
    OBSERVATION = "OBSERVATION"

    def __str__(self):
        return str(self.value)


OBSERVATION_SAMPLE_TYPE_NAMES = OrderedDict(
    [
        (OBSERVATION_SAMPLE_TYPE.BLOOD, "Blood"),
        (OBSERVATION_SAMPLE_TYPE.URINE, "Urine"),
        (OBSERVATION_SAMPLE_TYPE.URINE_DIPSTICK, "Urine Dipstick"),
        (OBSERVATION_SAMPLE_TYPE.OBSERVATION, "Observation"),
    ]
)


@log_changes
class Observation(db.Model):
    __tablename__ = "observations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    value_type = Column(
        EnumType(OBSERVATION_VALUE_TYPE, name="observation_value_type"), nullable=False
    )
    sample_type = Column(
        EnumType(OBSERVATION_SAMPLE_TYPE, name="observation_sample_type"),
        nullable=False,
    )
    pv_code = Column(String)

    min_value = Column(
        Numeric,
        CheckConstraint("min_value is null or value_type in ('REAL', 'INTEGER')"),
    )
    max_value = Column(
        Numeric,
        CheckConstraint(
            "min_value is null or max_value is null or max_value >= min_value"
        ),
        CheckConstraint("max_value is null or value_type in ('REAL', 'INTEGER')"),
    )
    min_length = Column(
        Integer,
        CheckConstraint("min_length is null or min_length > 0"),
        CheckConstraint("min_length is null or value_type = 'STRING'"),
    )
    max_length = Column(
        Integer,
        CheckConstraint("max_length is null or max_length > 0"),
        CheckConstraint(
            "min_length is null or max_length is null or max_length >= min_length"
        ),
        CheckConstraint("max_length is null or value_type = 'STRING'"),
    )
    units = Column(
        String,
        CheckConstraint("units is null or units != ''"),
        CheckConstraint("units is null or value_type in ('REAL', 'INTEGER')"),
    )
    options = Column(
        postgresql.ARRAY(String),
        CheckConstraint(
            """
            (value_type = 'ENUM' and coalesce(array_length(options, 1), 0) > 0 and array_length(options, 1) % 2 = 0) or
            (value_type != 'ENUM' and (options is null or coalesce(array_length(options, 1), 0) = 0))
        """
        ),
    )

    group_observations = relationship("GroupObservation")

    @property
    def groups(self):
        return [x.group for x in self.group_observations]

    @property
    def options_list(self):
        value = self.options

        if value is not None:
            value = pairwise(value)

        return value

    @options_list.setter
    def options_list(self, value):
        if value is not None:
            value = list(chain(*value))

        self.options = value

    @property
    def options_dict(self):
        value = self.options_list

        if value is not None:
            value = OrderedDict(value)

        return value

    @options_dict.setter
    def options_dict(self, value):
        if value is not None:
            value = value.items()

        self.options_list = value

    @property
    def option_codes(self):
        value = self.options_dict

        if value is None:
            value = []
        else:
            value = value.keys()

        return value

    @property
    def code_description_pairs(self):
        value = self.options_dict

        if value is None:
            value = []
        else:
            value = [{"code": k, "description": v} for k, v in value.items()]

        return value

    def __str__(self):
        return self.name


@event.listens_for(Observation, "before_insert")
@event.listens_for(Observation, "before_update")
def observation_update(mapper, connection, target):
    """Replace empty options value with None.

    There are constraints set on table not to allow empty values,
    it has to be either NULL or at least one pair of options. However,
    flask-admin sets that to empty list, if nothing is given and
    database throws an Integrity Error.
    """
    if not target.options:
        target.options = None


@log_changes
class Result(db.Model, MetaModelMixin):
    __tablename__ = "results"

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship("results")

    source_group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    source_group = relationship("Group")
    source_type = Column(String, nullable=False)

    observation_id = Column(Integer, ForeignKey("observations.id"), nullable=False)
    observation = relationship("Observation")

    date = Column(DateTime(timezone=True), nullable=False)
    _value = Column("value", String, nullable=True)
    sent_value = Column(String, nullable=False)

    @property
    def value(self):
        x = self._value

        if x is not None and self.observation is not None:
            value_type = self.observation.value_type

            # Values are stored as strings so need to be converted to the correct type

            if value_type == OBSERVATION_VALUE_TYPE.INTEGER:
                x = int(x)
            elif value_type == OBSERVATION_VALUE_TYPE.REAL:
                x = float(x)

        return x

    @value.setter
    def value(self, x):
        if x is not None:
            # Values are stored as strings
            x = str(x)

        self._value = x

    @property
    def value_label(self):
        if self.observation.value_type == OBSERVATION_VALUE_TYPE.ENUM:
            return self.observation.options_dict.get(self.value)
        else:
            return None

    @property
    def value_label_or_value(self):
        """Return value label if it is available, else value."""
        return self.value_label if self.value_label else self.sent_value

    @property
    def egfr_calculated(self):
        if self.observation.short_name.lower() != "creatinine" or not self.value:
            return ""

        creat88 = self.value / 88.4
        egfr = 0
        black_adj = 1

        ethnicity = self.patient.available_ethnicity
        if ethnicity and ethnicity.code in ("M", "N", "P"):
            black_adj = 1.159

        months = self.patient.to_age(
            date(self.date.year, self.date.month, self.date.day)
        )
        if not months:
            return ""

        years_old = months // 12
        age_adj = 0.993 ** years_old
        is_female = self.patient.radar_gender == GENDER_FEMALE
        is_male = self.patient.radar_gender == GENDER_MALE
        if is_female and creat88 > 0.7:
            egfr = age_adj * black_adj * 144 * ((creat88 / 0.7) ** (-1.209))
        elif is_female and creat88 <= 0.7:
            egfr = age_adj * black_adj * 144 * ((creat88 / 0.7) ** (-0.329))
        elif is_male and creat88 > 0.7:
            egfr = age_adj * black_adj * 141 * ((creat88 / 0.9) ** (-1.209))
        elif is_male and creat88 <= 0.7:
            egfr = age_adj * black_adj * 141 * ((creat88 / 0.9) ** (-0.411))

        return egfr
    
    @property
    def ckd_epi_egfr_calculated_with_ethnicity(self):
        if self.observation.short_name.lower() != "creatinine" or not self.value:
            return ""
        
        Scr = self.value * 0.0113
        coef_a = 141.0
        
        if self.patient.gender == 1:        
            kappa = 0.9
            alpha = -0.411
            coef_d = 1
        elif self.patient.gender == 2:
            kappa = 0.7
            alpha = -0.329
            coef_d = 1.018
        else:
            return ""

        coef_b = math.pow(min(Scr / kappa, 1.0), alpha)
        coef_c = math.pow(max(Scr / kappa, 1.0), -1.209)
        
        this_year = date.today().year
        age = this_year - self.patient.year_of_birth
        if age >= 18:
            age_coef = math.pow(0.993, age)
        else:
            return ""
        
        if self.patient.ethnicity in (12, 13, 14):
            coef_e = 1.159
        else:
            coef_e = 1

        egfr = coef_a * coef_b * coef_c * age_coef * coef_d * coef_e
        return int(round(egfr))

    @property
    def ckd_epi_egfr_calculated_without_ethnicity(self):
        if self.observation.short_name.lower() != "creatinine" or not self.value:
            return ""
        
        Scr = self.value * 0.0113
        coef_a = 141.0
        
        if self.patient.gender == 1:        
            kappa = 0.9
            alpha = -0.411
            coef_d = 1
        elif self.patient.gender == 2:
            kappa = 0.7
            alpha = -0.329
            coef_d = 1.018
        else:
            return ""

        coef_b = math.pow(min(Scr / kappa, 1.0), alpha)
        coef_c = math.pow(max(Scr / kappa, 1.0), -1.209)
        
        this_year = date.today().year
        age = this_year - self.patient.year_of_birth
        if age >= 18:
            age_coef = math.pow(0.993, age)
        else:
            return ""

        egfr = coef_a * coef_b * coef_c * age_coef * coef_d
        return int(round(egfr))
    
    @property
    def calculate_z_score_height(self):
        if self.observation.short_name.lower() != 'height':
            return ""
    

        this_year = date.today().year
        age = this_year - self.patient.year_of_birth
        if age <= 18:
            age_coef = math.pow(0.993, age)
        else:
            return ""



        if self.patient.age <= 16:
            print("do z_score calculation")
        else:
            z_score = None
        

        return z_score
    
    @property
    def calculate_z_score_weight(self):
        if self.observation.short_name.lower() != 'weight':
            return ""
        
        days_diff = (date.today() - self.patient.date_of_birth).day
        age_as_months = days_diff / 30.4375

        lower_age_band, upper_age_band = self._get_age_band_values('weight', age_as_months)

        actual_age_band = ((age_as_months - lower_age_band) / (upper_age_band - lower_age_band))
        actual_l = lower_age_band.l_value + (actual_age_band * (upper_age_band.l_value - lower_age_band.l_value))
        actual_median = lower_age_band.median_value + (actual_age_band * (upper_age_band.median_value - lower_age_band.median))
        actual_s = lower_age_band.s_value + (actual_age_band * (upper_age_band.s_value - lower_age_band.s_value))

        return (math.pow((self.value / actual_median), actual_l) - 1) / (actual_l * actual_s)
    
    def _get_age_band_values(self, type, age_as_months):
        temp_ages = db.session.query(z_score_constants.age_months).all()
        ages = np.asarray([age_tuple[0] for age_tuple in temp_ages])
        index = (np.abs(ages - age_as_months)).argmin()

        closest_age = ages[index]
        if closest_age > age_as_months:
            return ages[index - 1], closest_age
        else:
            return closest_age, ages[index + 1]



Index("results_patient_idx", Result.patient_id)


@log_changes
class GroupObservation(db.Model):
    __tablename__ = "group_observations"

    id = Column(Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    group = relationship("Group")

    observation_id = Column(Integer, ForeignKey("observations.id"), nullable=False)
    observation = relationship("Observation")

    weight = Column(Integer, CheckConstraint("weight > 0"))


Index("group_observations_group_idx", GroupObservation.group_id)
Index("group_observations_observation_idx", GroupObservation.observation_id)
Index(
    "group_observations_observation_group_idx",
    GroupObservation.observation_id,
    GroupObservation.group_id,
    unique=True,
)
