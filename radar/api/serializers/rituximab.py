from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer

from radar.api.serializers.common import (
    MetaMixin,
    PatientMixin,
    StringLookupField
)
from radar.models.rituximab import BaselineAssessment, NEPHROPATHIES, SUPPORTIVE_MEDICATIONS


class RituximabBaselineAssessmentSerializer(PatientMixin, MetaMixin, ModelSerializer):
    past_remission = fields.BooleanField(required=False)
    nephropathies = fields.ListField(required=False, child=StringLookupField(NEPHROPATHIES))
    supportive_medication = fields.ListField(required=False, child=StringLookupField(SUPPORTIVE_MEDICATIONS))

    class Meta(object):
        model_class = BaselineAssessment
        exclude = ['user_id']
