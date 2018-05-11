from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer

from radar.api.serializers.common import MetaMixin, PatientMixin
from radar.models.rituximab import BaselineAssessment


class RituximabBaselineAssessmentSerializer(PatientMixin, MetaMixin, ModelSerializer):
    # date = fields.DateField()
    # supportive_medication

    class Meta(object):
        model_class = BaselineAssessment
        exclude = ['user_id']
