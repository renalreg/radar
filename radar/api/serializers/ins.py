from cornflake import fields
from cornflake.exceptions import ValidationError
from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake.validators import max_length, none_if_blank, optional

from radar.api.serializers.common import MetaMixin, PatientMixin, StringLookupField
from radar.api.serializers.validators import valid_date_for_patient
from radar.models.ins import DIPSTICK_TYPES, InsClinicalPicture, InsRelapse, KIDNEY_TYPES, REMISSION_TYPES


class InsClinicalPictureSerializer(PatientMixin, MetaMixin, ModelSerializer):
    date_of_picture = fields.DateField()
    oedema = fields.BooleanField(required=False)
    hypovalaemia = fields.BooleanField(required=False)
    fever = fields.BooleanField(required=False)
    thrombosis = fields.BooleanField(required=False)
    peritonitis = fields.BooleanField(required=False)
    pulmonary_odemea = fields.BooleanField(required=False)
    hypertension = fields.BooleanField(required=False)
    rash = fields.BooleanField(required=False)
    rash_details = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])
    infection = fields.BooleanField(required=False)
    infection_details = fields.StringField(
        required=False,
        validators=[none_if_blank(), optional(), max_length(10000)]
    )
    ophthalmoscopy = fields.BooleanField(required=False)
    ophthalmoscopy_details = fields.StringField(
        required=False,
        validators=[none_if_blank(), optional(), max_length(10000)]
    )
    comments = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])

    class Meta(object):
        model_class = InsClinicalPicture
        validators = [valid_date_for_patient('date_of_picture')]

    def pre_validate(self, data):
        # Remove rash details if the patient didn't have a rash
        if not data['rash']:
            data['rash_details'] = None

        # Remove ophthalmoscopy details if a ophthalmoscopy test wan't performed
        if not data['ophthalmoscopy']:
            data['ophthalmoscopy_details'] = None

        # Remove infection details if no infection
        if not data['infection']:
            data['infection_details'] = None

        return data


class InsRelapseSerializer(PatientMixin, MetaMixin, ModelSerializer):
    date_of_relapse = fields.DateField()
    kidney_type = StringLookupField(KIDNEY_TYPES)
    viral_trigger = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])
    immunisation_trigger = fields.StringField(
        required=False,
        validators=[none_if_blank(), optional(), max_length(10000)]
    )
    other_trigger = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])
    peak_pcr = fields.FloatField(required=False)
    peak_acr = fields.FloatField(required=False)
    peak_protein_dipstick = StringLookupField(DIPSTICK_TYPES)
    remission_protein_dipstick = StringLookupField(DIPSTICK_TYPES)
    high_dose_oral_prednisolone = fields.BooleanField(required=False)
    iv_methyl_prednisolone = fields.BooleanField(required=False)
    date_of_remission = fields.DateField(required=False)
    remission_type = StringLookupField(REMISSION_TYPES, required=False)
    remission_pcr = fields.FloatField(required=False)
    remission_acr = fields.FloatField(required=False)

    class Meta(object):
        model_class = InsRelapse
        validators = [
            valid_date_for_patient('date_of_relapse'),
            valid_date_for_patient('date_of_remission'),
        ]

    def pre_validate(self, data):
        # Remove remission type if the date of remission is missing
        if not data['date_of_remission']:
            data['remission_type'] = None

        return data

    def validate(self, data):
        data = super(InsRelapseSerializer, self).validate(data)

        # Remission must be after relapse
        if data['date_of_remission'] is not None and data['date_of_remission'] < data['date_of_relapse']:
            raise ValidationError({'date_of_remission': 'Must be on or after date of relapse.'})

        return data
