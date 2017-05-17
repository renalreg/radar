from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer, ReferenceField

from radar.api.serializers.common import MetaMixin, PatientMixin
from radar.models.nurture_tubes import PROTOCOL_OPTION_TYPE, SampleOption, Samples

try:
    basestring
except NameError:
    basestring = str


class OptionSerializer(ModelSerializer):
    id = fields.EnumField(PROTOCOL_OPTION_TYPE)

    class Meta(object):
        model_class = SampleOption


class ProtocolField(ReferenceField):
    model_class = SampleOption
    serializer_class = OptionSerializer

    def to_internal_value(self, data):
        if isinstance(data, basestring):
            data = PROTOCOL_OPTION_TYPE(data)
        instance = self.get_instance(data)
        return instance


class SamplesSerializer(PatientMixin, MetaMixin, ModelSerializer):
    taken_on = fields.DateField()
    barcode = fields.IntegerField()
    protocol = ProtocolField()

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
