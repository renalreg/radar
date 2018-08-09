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
    RituximabCriteria,
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


class RituximabCriteriaSerializer(PatientMixin, MetaMixin, ModelSerializer):
    date = fields.DateField()

    therapy_failure = fields.BooleanField(required=False)
    hypersensitivity = fields.BooleanField(required=False)
    drug_associated_toxicity = fields.BooleanField(required=False)
    alkylating_complication = fields.BooleanField(required=False)
    alkylating_failure_monitoring_requirements = fields.BooleanField(required=False)
    cancer = fields.BooleanField(required=False)
    threatened_fertility = fields.BooleanField(required=False)
    fall_in_egfr = fields.BooleanField(required=False)
    cni_therapy_complication = fields.BooleanField(required=False)
    cni_failure_monitoring_requirements = fields.BooleanField(required=False)
    diabetes = fields.BooleanField(required=False)
    risk_factors = fields.BooleanField(required=False)

    class Meta(object):
        model_class = RituximabCriteria
