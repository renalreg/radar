from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake import fields

from radar.api.serializers.common import PatientMixin, MetaMixin
from radar.api.serializers.validators import valid_date_for_patient
from radar.models.renal_progressions import RenalProgression


class RenalProgressionSerializer(PatientMixin, MetaMixin, ModelSerializer):
    onset_date = fields.DateField(required=False)
    esrf_date = fields.DateField(required=False)

    class Meta(object):
        model_class = RenalProgression
        validators = [
            valid_date_for_patient('onset_date'),
            valid_date_for_patient('esrf_date'),
        ]
