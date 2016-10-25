from cornflake import fields
from cornflake.exceptions import ValidationError
from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake.validators import (
    range_,
    none_if_blank,
    optional,
    max_length,
    required
)

from radar.api.serializers.common import (
    PatientMixin,
    MetaMixin,
    SourceMixin,
    StringLookupField
)
from radar.api.serializers.validators import valid_date_for_patient
from radar.models.renal_imaging import (
    RenalImaging,
    RENAL_IMAGING_TYPES,
    RENAL_IMAGING_KIDNEY_TYPES
)


class RenalImagingSerializer(PatientMixin, SourceMixin, MetaMixin, ModelSerializer):
    date = fields.DateField()
    imaging_type = StringLookupField(RENAL_IMAGING_TYPES)

    right_present = fields.BooleanField(required=False)
    right_type = StringLookupField(RENAL_IMAGING_KIDNEY_TYPES, required=False)
    right_length = fields.FloatField(required=False, validators=[range_(1, 30)])
    right_volume = fields.FloatField(required=False)  # TODO range
    right_cysts = fields.BooleanField(required=False)
    right_stones = fields.BooleanField(required=False)
    right_calcification = fields.BooleanField(required=False)
    right_nephrocalcinosis = fields.BooleanField(required=False)
    right_nephrolithiasis = fields.BooleanField(required=False)
    right_other_malformation = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])

    left_present = fields.BooleanField(required=False)
    left_type = StringLookupField(RENAL_IMAGING_KIDNEY_TYPES, required=False)
    left_length = fields.FloatField(required=False, validators=[range_(1, 30)])
    left_volume = fields.FloatField(required=False)  # TODO range
    left_cysts = fields.BooleanField(required=False)
    left_stones = fields.BooleanField(required=False)
    left_calcification = fields.BooleanField(required=False)
    left_nephrocalcinosis = fields.BooleanField(required=False)
    left_nephrolithiasis = fields.BooleanField(required=False)
    left_other_malformation = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])

    class Meta(object):
        model_class = RenalImaging
        validators = [valid_date_for_patient('date')]

    def pre_validate(self, data):
        if not data['right_present']:
            data['right_type'] = None
            data['right_length'] = None
            data['right_volume'] = None
            data['right_cysts'] = None
            data['right_stones'] = None
            data['right_calcification'] = None
            data['right_nephrocalcinosis'] = None
            data['right_nephrolithiasis'] = None
            data['right_other_malformation'] = None
        elif not data['right_calcification']:
            data['right_nephrocalcinosis'] = None
            data['right_nephrolithiasis'] = None

        if not data['left_present']:
            data['left_type'] = None
            data['left_length'] = None
            data['left_volume'] = None
            data['left_cysts'] = None
            data['left_stones'] = None
            data['left_calcification'] = None
            data['left_nephrocalcinosis'] = None
            data['left_nephrolithiasis'] = None
            data['left_other_malformation'] = None
        elif not data['left_calcification']:
            data['left_nephrocalcinosis'] = None
            data['left_nephrolithiasis'] = None

        return data

    def validate(self, data):
        if data['right_present'] is None and data['left_present'] is None:
            raise ValidationError({
                'right_present': 'Either right or left must be present.',
                'left_present': 'Either right or left must be present.'
            })

        if data['right_present']:
            self.run_validators_on_field(data, 'right_type', [required()])
            self.run_validators_on_field(data, 'right_cysts', [required()])
            self.run_validators_on_field(data, 'right_stones', [required()])
            self.run_validators_on_field(data, 'right_calcification', [required()])

            if data['right_calcification']:
                self.run_validators_on_field(data, 'right_nephrocalcinosis', [required()])
                self.run_validators_on_field(data, 'right_nephrolithiasis', [required()])

        if data['left_present']:
            self.run_validators_on_field(data, 'left_type', [required()])
            self.run_validators_on_field(data, 'left_cysts', [required()])
            self.run_validators_on_field(data, 'left_stones', [required()])
            self.run_validators_on_field(data, 'left_calcification', [required()])

            if data['left_calcification']:
                self.run_validators_on_field(data, 'left_nephrocalcinosis', [required()])
                self.run_validators_on_field(data, 'left_nephrolithiasis', [required()])

        return data
