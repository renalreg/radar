from cornflake.sqlalchemy_orm import ModelSerializer

from radar.api.serializers.common import MetaMixin, PatientMixin
from radar.models.rituximab import BaselineAssessment


class RituximabBaselineAssessmentSerializer(PatientMixin, MetaMixin, ModelSerializer):

    class Meta(object):
        model_class = BaselineAssessment
        exclude = ['user_id']
