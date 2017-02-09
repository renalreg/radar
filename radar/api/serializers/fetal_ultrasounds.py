from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake.validators import max_length, none_if_blank, optional, range_

from radar.api.serializers.common import (
    MetaMixin,
    PatientMixin,
    SourceMixin,
    StringLookupField
)
from radar.api.serializers.validators import valid_date_for_patient
from radar.models.fetal_ultrasounds import FetalUltrasound, LIQUOR_VOLUMES


class FetalUltrasoundSerializer(PatientMixin, SourceMixin, MetaMixin, ModelSerializer):
    date_of_scan = fields.DateField()
    fetal_identifier = fields.StringField(required=False, validators=[max_length(30)])
    gestational_age = fields.IntegerField(validators=[range_(8 * 7, 42 * 7, 'days')])
    head_centile = fields.IntegerField(required=False, validators=[range_(0, 100)])
    abdomen_centile = fields.IntegerField(required=False, validators=[range_(0, 100)])
    uterine_artery_notched = fields.BooleanField(required=False)
    liquor_volume = StringLookupField(LIQUOR_VOLUMES, required=False)
    comments = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])

    class Meta(object):
        model_class = FetalUltrasound
        validators = [
            valid_date_for_patient('date_of_scan')
        ]
