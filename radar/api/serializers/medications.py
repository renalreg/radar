from cornflake import fields
from cornflake.exceptions import ValidationError
from cornflake.sqlalchemy_orm import ModelSerializer, ReferenceField
from cornflake.validators import max_length, min_, none_if_blank, optional, required

from radar.api.serializers.common import (
    MetaMixin,
    PatientMixin,
    SourceMixin,
    StringLookupField,
)
from radar.api.serializers.validators import valid_date_for_patient
from radar.models.medications import (
    CurrentMedication,
    Drug,
    DrugGroup,
    Medication,
    MEDICATION_DOSE_UNITS,
    MEDICATION_ROUTES
)


class DrugGroupSerializer(ModelSerializer):
    class Meta(object):
        model_class = DrugGroup
        exclude = ['parent_drug_group_id']


class DrugGroupField(ReferenceField):
    model_class = DrugGroup
    serializer_class = DrugGroupSerializer


class DrugSerializer(ModelSerializer):
    drug_group = DrugGroupField()

    class Meta(object):
        model_class = Drug
        exclude = ['drug_group_id']


class DrugField(ReferenceField):
    model_class = Drug
    serializer_class = DrugSerializer


class MedicationSerializer(PatientMixin, SourceMixin, MetaMixin, ModelSerializer):
    from_date = fields.DateField()
    to_date = fields.DateField(required=False)
    drug = DrugField(required=False)
    dose_quantity = fields.FloatField(required=False, validators=[min_(0)])
    dose_unit = StringLookupField(MEDICATION_DOSE_UNITS, required=False)
    frequency = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(1000)])
    route = StringLookupField(MEDICATION_ROUTES, required=False)
    drug_text = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])
    dose_text = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])

    class Meta(object):
        model_class = Medication
        exclude = ['drug_id']
        validators = [
            valid_date_for_patient('from_date'),
            valid_date_for_patient('to_date'),
        ]

    def pre_validate(self, data):
        # Coded drug overrides drug free-text
        if data['drug']:
            data['drug_text'] = None

        return data

    def validate(self, data):
        data = super(MedicationSerializer, self).validate(data)

        # To date must be after from date
        if data['to_date'] is not None and data['to_date'] < data['from_date']:
            raise ValidationError({'to_date': 'Must be on or after from date.'})

        # Must specify either a coded drug or a free-text drug
        if data['drug'] is None and data['drug_text'] is None:
            raise ValidationError({
                'drug': 'Must specify a drug.',
                'drug_text': 'Must specify a drug.',
            })

        # Coded dose quantities must have a unit
        if data['dose_quantity'] is not None:
            self.run_validators_on_field(data, 'dose_unit', [required()])

        return data


class CurrentMedicationSerializer(PatientMixin, SourceMixin, MetaMixin, ModelSerializer):
    date_recorded = fields.DateField()
    drug = DrugField(required=False)
    dose_quantity = fields.FloatField(required=False, validators=[min_(0)])
    dose_unit = StringLookupField(MEDICATION_DOSE_UNITS, required=False)
    frequency = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(1000)])
    route = StringLookupField(MEDICATION_ROUTES, required=False)
    drug_text = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])
    dose_text = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])

    class Meta(object):
        model_class = CurrentMedication
        exclude = ['drug_id']
        validators = [
            valid_date_for_patient('date_recorded'),
        ]

    def pre_validate(self, data):
        # Coded drug overrides drug free-text
        if data['drug']:
            data['drug_text'] = None

        return data

    def validate(self, data):
        data = super(CurrentMedicationSerializer, self).validate(data)

        # Must specify either a coded drug or a free-text drug
        if data['drug'] is None and data['drug_text'] is None:
            raise ValidationError({
                'drug': 'Must specify a drug.',
                'drug_text': 'Must specify a drug.',
            })

        # Coded dose quantities must have a unit
        if data['dose_quantity'] is not None:
            self.run_validators_on_field(data, 'dose_unit', [required()])

        return data
