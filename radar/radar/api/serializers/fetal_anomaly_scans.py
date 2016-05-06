from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake import fields
from cornflake.validators import none_if_blank, optional, max_length, not_in_future, range_

from radar.serializers.common import PatientMixin, SourceMixin, MetaMixin
from radar.models.fetal_anomaly_scans import FetalAnomalyScan


class FetalAnomalyScanSerializer(PatientMixin, SourceMixin, MetaMixin, ModelSerializer):
    date_of_scan = fields.DateField(validators=[not_in_future()])
    gestational_age = fields.IntegerField(validators=[range_(8 * 7, 42 * 7, 'days')])
    oligohydramnios = fields.BooleanField(required=False)
    right_anomaly_details = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])
    right_ultrasound_details = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])
    left_anomaly_details = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])
    left_ultrasound_details = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])

    class Meta(object):
        model_class = FetalAnomalyScan
