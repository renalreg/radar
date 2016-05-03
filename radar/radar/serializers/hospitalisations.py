from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake import fields
from cornflake.exceptions import ValidationError
from cornflake.validators import none_if_blank, optional, max_length

from radar.serializers.common import PatientMixin, SourceMixin, MetaMixin
from radar.models.plasmapheresis import Hospitalisation
from radar.serializers.validators import valid_date_for_patient


class HospitalisationSerializer(PatientMixin, SourceMixin, MetaMixin, ModelSerializer):
    date_of_admission = fields.DateField()
    date_of_discharge = fields.DateField(required=False)
    reason_for_admission = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])
    comments = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])

    class Meta(object):
        model_class = Hospitalisation
        validators = [
            valid_date_for_patient('date_of_admission'),
            valid_date_for_patient('date_of_discharge'),
        ]

    def validate(self, data):
        data = super(HospitalisationSerializer, self).validate(data)

        if data['date_of_discharge'] is not None and data['date_of_discharge'] < data['date_of_admission']:
            raise ValidationError({'date_of_discharge': 'Must be on or after from date of admission.'})

        return data
