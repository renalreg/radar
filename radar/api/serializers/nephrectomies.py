from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer

from radar.api.serializers.common import (
    MetaMixin,
    PatientMixin,
    SourceMixin,
    StringLookupField,
)
from radar.api.serializers.validators import valid_date_for_patient
from radar.models.nephrectomies import (
    Nephrectomy,
    NEPHRECTOMY_ENTRY_TYPES,
    NEPHRECTOMY_KIDNEY_SIDES,
    NEPHRECTOMY_KIDNEY_TYPES,
)


class NephrectomySerializer(PatientMixin, SourceMixin, MetaMixin, ModelSerializer):
    date = fields.DateField()
    kidney_side = StringLookupField(NEPHRECTOMY_KIDNEY_SIDES)
    kidney_type = StringLookupField(NEPHRECTOMY_KIDNEY_TYPES)
    entry_type = StringLookupField(NEPHRECTOMY_ENTRY_TYPES)

    class Meta(object):
        model_class = Nephrectomy
        validators = [valid_date_for_patient('date')]
