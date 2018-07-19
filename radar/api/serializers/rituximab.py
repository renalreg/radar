from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer

from radar.api.serializers.common import (
    MetaMixin,
    PatientMixin,
    SourceMixin,
    StringLookupField,
)
from radar.models.rituximab import (
    BaselineAssessment,
    NEPHROPATHY_TYPES,
    RituximabConsent,
    SUPPORTIVE_MEDICATIONS,
)


class RituximabBaselineAssessmentSerializer(PatientMixin, SourceMixin, MetaMixin, ModelSerializer):
    date = fields.DateField()
    past_remission = fields.BooleanField(required=False)
    nephropathy = StringLookupField(NEPHROPATHY_TYPES, required=False)
    supportive_medication = fields.ListField(
        required=False,
        child=StringLookupField(SUPPORTIVE_MEDICATIONS)
    )
    previous_treatment = fields.Field(required=False)
    steroids = fields.BooleanField(required=False)
    other_previous_treatment = fields.StringField(required=False)
    performance_status = fields.IntegerField(required=False)

    class Meta(object):
        model_class = BaselineAssessment

    def pre_validate(self, data):
        previous_treatment = data.get('previous_treatment')
        if previous_treatment:
            for key in list(previous_treatment.keys()):
                if not previous_treatment.get(key, {}).get(key, False):
                    data['previous_treatment'].pop(key, None)

        return data


class RituximabConsentSerializer(PatientMixin, MetaMixin, ModelSerializer):
    date = fields.DateField()

    class Meta(object):
        model_class = RituximabConsent
