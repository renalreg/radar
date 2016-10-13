from cornflake import fields
from cornflake.exceptions import ValidationError
from cornflake.sqlalchemy_orm import ModelSerializer

from radar.api.serializers.common import (
    PatientMixin,
    SourceMixin,
    MetaMixin,
    IntegerLookupField
)
from radar.api.serializers.validators import valid_date_for_patient
from radar.models.dialysis import Dialysis, DIALYSIS_MODALITIES


class DialysisSerializer(PatientMixin, SourceMixin, MetaMixin, ModelSerializer):
    from_date = fields.DateField()
    to_date = fields.DateField(required=False)
    modality = IntegerLookupField(DIALYSIS_MODALITIES)

    class Meta(object):
        model_class = Dialysis
        validators = [
            valid_date_for_patient('from_date'),
            valid_date_for_patient('to_date'),
        ]

    def validate(self, data):
        data = super(DialysisSerializer, self).validate(data)

        # Check to date is after from date
        if data['to_date'] is not None and data['to_date'] < data['from_date']:
            raise ValidationError({'to_date': 'Must be on or after from date.'})

        return data
