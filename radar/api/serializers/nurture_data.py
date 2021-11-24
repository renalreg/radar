from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer

from radar.api.serializers.common import MetaMixin, PatientMixin
from radar.models.nurture_data import NurtureData


class NurtureDataSerializer(MetaMixin, PatientMixin, ModelSerializer):
    patient_id = fields.IntegerField(required=False)
    signed_off_state = fields.IntegerField(required=False)
    blood_tests = fields.BooleanField()
    interviews = fields.BooleanField()

    class Meta(object):
        model_class = NurtureData
