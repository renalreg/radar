from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake.validators import max_length, none_if_blank, optional

from radar.api.serializers.common import IntegerLookupField, MetaMixin, PatientMixin
from radar.api.serializers.validators import valid_date_for_patient
from radar.models.alport import AlportClinicalPicture, DEAFNESS_NO, DEAFNESS_OPTIONS


class AlportClinicalPictureSerializer(PatientMixin, MetaMixin, ModelSerializer):
    date_of_picture = fields.DateField()
    deafness = IntegerLookupField(DEAFNESS_OPTIONS)
    deafness_date = fields.DateField(required=False)
    hearing_aid_date = fields.DateField(required=False)
    comments = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])

    class Meta(object):
        model_class = AlportClinicalPicture
        validators = [
            valid_date_for_patient('date_of_picture'),
            valid_date_for_patient('deafness_date'),
            valid_date_for_patient('hearing_aid_date'),
        ]

    def pre_validate(self, data):
        # Not deaf
        if data['deafness'] == DEAFNESS_NO:
            data['deafness_date'] = None
            data['hearing_aid_date'] = None

        return data
