from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake import fields
from cornflake.validators import none_if_blank, optional, max_length

from radar.api.serializers.common import PatientMixin, MetaMixin, StringLookupField, IntegerLookupField
from radar.api.serializers.validators import valid_date_for_patient
from radar.models.fuan import FuanClinicalPicture, THP_RESULTS, RELATIVES


class FuanClinicalPictureSerializer(PatientMixin, MetaMixin, ModelSerializer):
    picture_date = fields.DateField()
    gout = fields.BooleanField(required=False)
    gout_date = fields.DateField(required=False)
    family_gout = fields.BooleanField(required=False)
    family_gout_relatives = fields.ListField(required=False, child=IntegerLookupField(RELATIVES))
    thp = StringLookupField(THP_RESULTS, required=False)
    uti = fields.BooleanField(required=False)
    comments = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])

    def pre_validate(self, data):
        if not data['gout']:
            data['gout_date'] = None

        if not data['family_gout']:
            data['family_gout_relatives'] = []

        return data

    class Meta(object):
        model_class = FuanClinicalPicture
        validators = [
            valid_date_for_patient('picture_date'),
            valid_date_for_patient('gout_date')
        ]
