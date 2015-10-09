from radar.models import Patient
from radar.serializers.models import ReferenceField


class PatientReferenceField(ReferenceField):
    model_class = Patient
