from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake import fields
from cornflake.validators import none_if_blank, optional, max_length

from radar.api.serializers.common import PatientMixin, MetaMixin
from radar.api.serializers.validators import valid_date_for_patient
from radar.models.mpgn import MpgnClinicalPicture


class MpgnClinicalPictureSerializer(PatientMixin, MetaMixin, ModelSerializer):
    date_of_picture = fields.DateField()
    oedema = fields.BooleanField(required=False)
    hypertension = fields.BooleanField(required=False)
    urticaria = fields.BooleanField(required=False)
    partial_lipodystrophy = fields.BooleanField(required=False)
    infection = fields.BooleanField(required=False)
    infection_details = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])
    ophthalmoscopy = fields.BooleanField(required=False)
    ophthalmoscopy_details = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])
    comments = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(5000)])

    class Meta(object):
        model_class = MpgnClinicalPicture
        validators = [valid_date_for_patient('date_of_picture')]

    def pre_validate(self, data):
        # Remove infection details if the patient didn't have an infection
        if not data['infection']:
            data['infection_details'] = None

        # Remove ophthalmoscopy details if a ophthalmoscopy test wan't performed
        if not data['ophthalmoscopy']:
            data['ophthalmoscopy_details'] = None

        return data
