from cornflake.sqlalchemy_orm import ModelSerializer, ReferenceField
from cornflake import fields
from cornflake.validators import none_if_blank, optional, max_length, min_, required
from cornflake.exceptions import ValidationError

from radar.serializers.common import PatientMixin, MetaMixin, SourceMixin
from radar.serializers.validators import valid_date_for_patient
from radar.models.medications import Medication, Drug, MEDICATION_DOSE_UNITS, MEDICATION_ROUTES


class ParentDrugSerializer(ModelSerializer):
    class Meta(object):
        model_class = Drug
        exclude = ['parent_drug_id']


class ParentDrugField(ReferenceField):
    model_class = Drug
    serializer_class = ParentDrugSerializer


class DrugSerializer(ModelSerializer):
    parent_drug = ParentDrugField()

    class Meta(object):
        model_class = Drug
        exclude = ['parent_drug_id']


class DrugField(ReferenceField):
    model_class = Drug
    serializer = DrugSerializer


class MedicationSerializer(PatientMixin, SourceMixin, MetaMixin, ModelSerializer):
    from_date = fields.DateField()
    to_date = fields.DateField(required=False)
    drug = DrugField(required=False)
    dose_quantity = fields.FloatField(required=False, validators=min_(0))
    dose_unit = fields.StringLookupField(MEDICATION_DOSE_UNITS, required=False)
    frequency = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(1000)])
    route = fields.StringLookupField(MEDICATION_ROUTES, required=False)
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

        if data['to_date'] is not None and data['to_date'] < data['from_date']:
            raise ValidationError({'to_date': 'Must be on or after from date.'})

        if data['drug'] is None and data['drug_text'] is None:
            raise ValidationError({
                'drug': 'Must specify a drug.',
                'drug_text': 'Must specify a drug.',
            })

        if data['dose_quantity'] is not None:
            self.run_validators_on_field(data, self.dose_unit, [required()])

        return data
