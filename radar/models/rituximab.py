from collections import OrderedDict

from sqlalchemy import Column, Date, Integer
from sqlalchemy.dialects import postgresql

from radar.database import db
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship, uuid_pk_column
from radar.models.logs import log_changes


PERFORMANCE_STATUS_OPTIONS = OrderedDict([
    (0, '0: able to carry out all normal activity without restriction'),
    (1, '1: restricted in strenuous activity but ambulatory and able to carry out light work'),
    (2, '2: ambulatory and capable of all self-care but unable to carry out any work activities; up and about more than 50% of waking hours'),  # noqa
    (3, '3: symptomatic and in a chair or in bed for greater than 50% of the day but not bedridden'),
    (4, '4: completely disabled; cannot carry out any self-care; totally confined to bed or chair'),
])


TREATMENT_OPTIONS = OrderedDict([
    ('chlorambucil', 'Chlorambucil'),
    ('cyclophosphamide', 'Cyclophosphamide'),
    ('rituximab', 'Rituximab'),
    ('tacrolimus', 'Tacrolimus'),
    ('cyclosporine', 'Cyclosporine'),
    ('steroids', 'Steroids'),
])


@log_changes
class BaselineAssessment(db.Model, MetaModelMixin):
    __tablename__ = 'rituximab_baseline_assessment'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('rituximab_baseline_assessment')

    date = Column(Date, nullable=False)

    supportive_medication = Column(postgresql.JSONB)  # [{}, ]
    previous_treatment = Column(postgresql.JSONB)  # [{'name': '', 'start': '', 'end': ''}, ]
    performance_status = Column(Integer)

    # @property
    # def performance_status_label(self):
    #     status = self.performance_status
    #     label = PERFORMANCE_STATUS_LABELS.get(status)
    #     return '{}: {}'.format(status, label)
