from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer

from radar.api.serializers.common import MetaMixin, PatientMixin, SystemSourceMixin
from radar.models import IndiaEthnicity


class IndiaEthnicitySerializer(PatientMixin, SystemSourceMixin, MetaMixin, ModelSerializer):
    father_ancestral_state = fields.StringField(required=False)
    father_language = fields.StringField(required=False)
    mother_ancestral_state = fields.StringField(required=False)
    mother_language = fields.StringField(required=False)

    class Meta(object):
        model_class = IndiaEthnicity
