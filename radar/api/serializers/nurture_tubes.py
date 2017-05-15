from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer

from radar.api.serializers.common import EnumLookupField, MetaMixin, PatientMixin, StringLookupField
from radar.models.nurture_tubes import PROTOCOL_OPTION_TYPE, PROTOCOL_OPTION_TYPE_NAMES, SampleOption, Samples


class SamplesSerializer(PatientMixin, MetaMixin, ModelSerializer):
    taken_on = fields.DateField()
    barcode = fields.IntegerField()
    protocol = fields.StringField()

    epa = fields.IntegerField(required=False)
    epb = fields.IntegerField(required=False)
    lpa = fields.IntegerField(required=False)
    lpb = fields.IntegerField(required=False)
    uc = fields.IntegerField(required=False)
    ub = fields.IntegerField(required=False)
    ud = fields.IntegerField(required=False)
    fub = fields.IntegerField(required=False)
    sc = fields.IntegerField(required=False)
    sa = fields.IntegerField(required=False)
    sb = fields.IntegerField(required=False)
    rna = fields.IntegerField(required=False)
    wb = fields.IntegerField(required=False)

    class Meta(object):
        model_class = Samples


class OptionSerializer(ModelSerializer):

    class Meta(object):
        model_class = SampleOption
