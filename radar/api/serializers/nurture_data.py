from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer

from radar.api.serializers.common import MetaMixin, PatientMixin
from radar.models.nurture_data import NurtureData


class NurtureDataSerializer(MetaMixin, PatientMixin, ModelSerializer):
    patient_id = fields.IntegerField(required=False)
    signed_off_state = fields.IntegerField(required=False)
    follow_up_refused_date = fields.DateField(required=False)
    blood_tests = fields.BooleanField()
    blood_refused_date = fields.DateField(required=False)
    interviews = fields.BooleanField()
    interviews_refused_date = fields.DateField(required=False)

    class Meta(object):
        model_class = NurtureData
