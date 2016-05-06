from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake import fields
from cornflake.exceptions import ValidationError

from radar.api.serializers.common import PatientMixin, SourceMixin, MetaMixin
from radar.models.plasmapheresis import Plasmapheresis, PLASMAPHERESIS_NO_OF_EXCHANGES, PLASMAPHERESIS_RESPONSES
from radar.api.serializers.validators import valid_date_for_patient


class PlasmapheresisSerializer(PatientMixin, SourceMixin, MetaMixin, ModelSerializer):
    from_date = fields.DateField()
    to_date = fields.DateField(required=False)
    no_of_exchanges = fields.StringLookupField(PLASMAPHERESIS_NO_OF_EXCHANGES, required=False)
    response = fields.StringLookupField(PLASMAPHERESIS_RESPONSES, required=False)

    class Meta(object):
        model_class = Plasmapheresis
        validators = [
            valid_date_for_patient('from_date'),
            valid_date_for_patient('to_date'),
        ]

    def validate(self, data):
        data = super(PlasmapheresisSerializer, self).validate(data)

        if data['to_date'] is not None and data['to_date'] < data['from_date']:
            raise ValidationError({'to_date': 'Must be on or after from date.'})

        return data
