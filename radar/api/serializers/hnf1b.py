from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake import fields
from cornflake.validators import none_if_blank, optional, max_length

from radar.api.serializers.common import PatientMixin, MetaMixin
from radar.api.serializers.validators import valid_date_for_patient
from radar.models.hnf1b import Hnf1bClinicalPicture


class Hnf1bClinicalPictureSerializer(PatientMixin, MetaMixin, ModelSerializer):
    date_of_picture = fields.DateField()
    single_kidney = fields.BooleanField(required=False)
    hyperuricemia_gout = fields.BooleanField(required=False)
    genital_malformation = fields.BooleanField(required=False)
    genital_malformation_details = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])
    familial_cystic_disease = fields.BooleanField(required=False)
    hypertension = fields.BooleanField(required=False)

    class Meta(object):
        model_class = Hnf1bClinicalPicture
        validators = [valid_date_for_patient('date_of_picture')]
