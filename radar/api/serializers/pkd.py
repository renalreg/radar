from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake import fields
from cornflake.validators import range_
from cornflake.exceptions import ValidationError

from radar.api.serializers.common import (
    PatientMixin,
    MetaMixin,
    SourceMixin,
    StringLookupField
)
from radar.api.serializers.validators import valid_date_for_patient
from radar.models.pkd import (
    LiverImaging,
    LIVER_IMAGING_TYPES,
    LiverDiseases,
    LiverTransplant,
    FIRST_GRAFT_SOURCES,
    LOSS_REASONS,
    INDICATIONS
)


class LiverImagingSerializer(PatientMixin, SourceMixin, MetaMixin, ModelSerializer):
    date = fields.DateField()
    imaging_type = StringLookupField(LIVER_IMAGING_TYPES)
    size = fields.FloatField(required=False, validators=[range_(0, 100, 'cm')])
    hepatic_fibrosis = fields.BooleanField(required=False)
    hepatic_cysts = fields.BooleanField(required=False)
    bile_duct_cysts = fields.BooleanField(required=False)
    dilated_bile_ducts = fields.BooleanField(required=False)
    cholangitis = fields.BooleanField(required=False)

    class Meta(object):
        model_class = LiverImaging
        validators = [valid_date_for_patient('date')]


class LiverDiseasesSerializer(PatientMixin, MetaMixin, ModelSerializer):
    portal_hypertension = fields.BooleanField(required=False)
    portal_hypertension_date = fields.DateField(required=False)
    oesophageal = fields.BooleanField(required=False)
    oesophageal_date = fields.DateField(required=False)
    oesophageal_bleeding = fields.BooleanField(required=False)
    oesophageal_bleeding_date = fields.DateField(required=False)
    gastric = fields.BooleanField(required=False)
    gastric_date = fields.DateField(required=False)
    gastric_bleeding = fields.BooleanField(required=False)
    gastric_bleeding_date = fields.DateField(required=False)
    anorectal = fields.BooleanField(required=False)
    anorectal_date = fields.DateField(required=False)
    anorectal_bleeding = fields.BooleanField(required=False)
    anorectal_bleeding_date = fields.DateField(required=False)
    cholangitis_acute = fields.BooleanField(required=False)
    cholangitis_acute_date = fields.DateField(required=False)
    cholangitis_recurrent = fields.BooleanField(required=False)
    cholangitis_recurrent_date = fields.DateField(required=False)
    spleen_palpable = fields.BooleanField(required=False)
    spleen_palpable_date = fields.DateField(required=False)

    class Meta(object):
        model_class = LiverDiseases
        validators = [
            valid_date_for_patient('portal_hypertension_date'),
            valid_date_for_patient('oesophageal_date'),
            valid_date_for_patient('oesophageal_bleeding_date'),
            valid_date_for_patient('gastric_date'),
            valid_date_for_patient('gastric_bleeding_date'),
            valid_date_for_patient('anorectal_date'),
            valid_date_for_patient('anorectal_bleeding_date'),
            valid_date_for_patient('cholangitis_acute_date'),
            valid_date_for_patient('cholangitis_recurrent_date'),
            valid_date_for_patient('spleen_palpable_date'),
        ]

    def pre_validate(self, data):
        pairs = [
            ('portal_hypertension', 'portal_hypertension_date'),
            ('oesophageal', 'oesophageal_date'),
            ('oesophageal_bleeding', 'oesophageal_bleeding_date'),
            ('gastric', 'gastric_date'),
            ('gastric_bleeding', 'gastric_bleeding_date'),
            ('anorectal', 'anorectal_date'),
            ('anorectal_bleeding', 'anorectal_bleeding_date'),
            ('cholangitis_acute', 'cholangitis_acute_date'),
            ('cholangitis_recurrent', 'cholangitis_recurrent_date'),
            ('spleen_palpable', 'spleen_palpable_date'),
        ]

        for a, b in pairs:
            if not data[a]:
                data[b] = None

        return data


class LiverTransplantSerializer(PatientMixin, SourceMixin, MetaMixin, ModelSerializer):
    registration_date = fields.DateField(required=False)
    transplant_date = fields.DateField()
    indications = fields.ListField(required=False, child=StringLookupField(INDICATIONS))
    other_indications = fields.StringField(required=False)
    first_graft_source = StringLookupField(FIRST_GRAFT_SOURCES, required=False)
    loss_reason = StringLookupField(LOSS_REASONS, required=False)
    other_loss_reason = fields.StringField(required=False)

    class Meta(object):
        model_class = LiverTransplant
        validators = [
            valid_date_for_patient('registration_date'),
            valid_date_for_patient('transplant_date'),
        ]

    def validate(self, data):
        data = super(LiverTransplantSerializer, self).validate(data)

        if data['registration_date'] is not None and data['transplant_date'] < data['registration_date']:
            raise ValidationError({'transplant_date': 'Must be on or after registration date.'})

        return data
