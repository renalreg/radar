from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake.validators import max_length, none_if_blank, optional

from radar.api.serializers.common import CohortGroupMixin, IntegerLookupField, MetaMixin, PatientMixin
from radar.api.serializers.validators import valid_date_for_patient
from radar.models.genetics import Genetics, GENETICS_KARYOTYPES


class GeneticsSerializer(PatientMixin, CohortGroupMixin, MetaMixin, ModelSerializer):
    date_sent = fields.DateField()
    laboratory = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(100)])
    reference_number = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(100)])
    karyotype = IntegerLookupField(GENETICS_KARYOTYPES, required=False)
    results = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])
    summary = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])

    class Meta(object):
        model_class = Genetics
        validators = [valid_date_for_patient('date_sent')]
