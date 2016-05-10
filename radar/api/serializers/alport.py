from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer

from radar.api.serializers.common import PatientMixin, MetaMixin, IntegerLookupField
from radar.api.serializers.validators import valid_date_for_patient
from radar.models.alport import AlportClinicalPicture, DEAFNESS_OPTIONS, DEAFNESS_NO


class AlportClinicalPictureSerializer(PatientMixin, MetaMixin, ModelSerializer):
    date_of_picture = fields.DateField()
    deafness = IntegerLookupField(DEAFNESS_OPTIONS)
    deafness_date = fields.DateField(required=False)
    hearing_aid_date = fields.DateField(required=False)

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
