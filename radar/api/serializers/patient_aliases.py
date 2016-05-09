from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake import fields
from cornflake.validators import not_empty, normalise_whitespace, upper, max_length

from radar.api.serializers.common import PatientMixin, RadarSourceMixin, MetaMixin
from radar.models.patient_aliases import PatientAlias


class PatientAliasSerializer(PatientMixin, RadarSourceMixin, MetaMixin, ModelSerializer):
    first_name = fields.StringField(validators=[not_empty(), normalise_whitespace(), upper(), max_length(100)])
    last_name = fields.StringField(validators=[not_empty(), normalise_whitespace(), upper(), max_length(100)])

    class Meta(object):
        model_class = PatientAlias
