from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake import fields
from cornflake.validators import range_

from radar.api.serializers.common import (
    PatientMixin,
    MetaMixin,
    SourceMixin,
    StringLookupField
)
from radar.api.serializers.validators import valid_date_for_patient
from radar.models.pkd import LiverImaging, LIVER_IMAGING_TYPES


class LiverImagingSerializer(PatientMixin, SourceMixin, MetaMixin, ModelSerializer):
    date = fields.DateField()
    imaging_type = StringLookupField(LIVER_IMAGING_TYPES)
    size = fields.FloatField(required=False, validators=[range_(0, 100, 'cm')])
    hepatic_fibrosis = fields.BooleanField(required=False)
    hepatic_cysts = fields.BooleanField(required=False)
    bile_duct_cysts = fields.BooleanField(required=False)
    dilated_bile_ducts = fields.BooleanField(required=False)
    cholangitis = fields.BooleanField(required=False)

    class Meta(object):
        model_class = LiverImaging
        validators = [valid_date_for_patient('date')]
