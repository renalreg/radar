from cornflake import fields
from cornflake.exceptions import ValidationError
from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake.validators import max_length, none_if_blank, optional

from radar.api.serializers.common import MetaMixin, PatientMixin, SourceMixin
from radar.api.serializers.validators import valid_date_for_patient
from radar.models.hospitalisations import Hospitalisation


class HospitalisationSerializer(PatientMixin, SourceMixin, MetaMixin, ModelSerializer):
    date_of_admission = fields.DateField()
    date_of_discharge = fields.DateField(required=False)
    reason_for_admission = fields.StringField(
        required=False,
        validators=[none_if_blank(), optional(), max_length(10000)]
    )
    comments = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])

    class Meta(object):
        model_class = Hospitalisation
        validators = [
            valid_date_for_patient('date_of_admission'),
            valid_date_for_patient('date_of_discharge'),
        ]

    def validate(self, data):
        data = super(HospitalisationSerializer, self).validate(data)

        # Can't be discharged before being admitted
        if data['date_of_discharge'] is not None and data['date_of_discharge'] < data['date_of_admission']:
            raise ValidationError({'date_of_discharge': 'Must be on or after from date of admission.'})

        return data
