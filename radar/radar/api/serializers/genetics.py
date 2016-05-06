from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake import fields
from cornflake.validators import none_if_blank, optional, max_length

from radar.serializers.common import PatientMixin, CohortGroupMixin, MetaMixin
from radar.models.genetics import Genetics, GENETICS_KARYOTYPES
from radar.serializers.validators import valid_date_for_patient


class GeneticsSerializer(PatientMixin, CohortGroupMixin, MetaMixin, ModelSerializer):
    date_sent = fields.DateField()
    laboratory = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(100)])
    reference_number = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(100)])
    karyotype = fields.IntegerLookupField(GENETICS_KARYOTYPES, required=False)
    results = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])
    summary = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])

    class Meta(object):
        model_class = Genetics
        validators = [valid_date_for_patient('date_sent')]
