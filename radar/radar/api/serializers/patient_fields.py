from radar.lib.models import Patient
from radar.lib.serializers.models import ReferenceField


class PatientReferenceField(ReferenceField):
    model_class = Patient
