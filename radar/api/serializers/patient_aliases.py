from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake.validators import max_length, normalise_whitespace, not_empty, upper

from radar.api.serializers.common import MetaMixin, PatientMixin, SystemSourceMixin
from radar.models.patient_aliases import PatientAlias


class PatientAliasSerializer(PatientMixin, SystemSourceMixin, MetaMixin, ModelSerializer):
    first_name = fields.StringField(validators=[not_empty(), normalise_whitespace(), upper(), max_length(100)])
    last_name = fields.StringField(validators=[not_empty(), normalise_whitespace(), upper(), max_length(100)])

    class Meta(object):
        model_class = PatientAlias
